// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
////////////////////////////////////////////////////////////////////////////////

// Package monitoringutil implements utility functions for monitoring.
package monitoringutil

import (
	"fmt"
	"strings"

	"github.com/google/tink/go/core/primitiveset"
	"github.com/google/tink/go/monitoring"
	tpb "github.com/google/tink/go/proto/tink_go_proto"
)

const keytypeURLPrefix = "type.googleapis.com/google.crypto."

// DoNothingLogger is a Logger that does nothing when invoked.
type DoNothingLogger struct{}

var _ monitoring.Logger = (*DoNothingLogger)(nil)

// Log drops a log call.
func (l *DoNothingLogger) Log(uint32, int) {}

// LogFailure drops a failure call.
func (l *DoNothingLogger) LogFailure() {}

func keyStatusFromProto(status tpb.KeyStatusType) (monitoring.KeyStatus, error) {
	var keyStatus monitoring.KeyStatus = 55
	switch status {
	case tpb.KeyStatusType_ENABLED:
		keyStatus = monitoring.Enabled
	case tpb.KeyStatusType_DISABLED:
		keyStatus = monitoring.Disabled
	case tpb.KeyStatusType_DESTROYED:
		keyStatus = monitoring.Destroyed
	default:
		return keyStatus, fmt.Errorf("unknown key status: %q", status)
	}
	return keyStatus, nil

}

func parseKeyTypeURL(ktu string) string {
	return strings.TrimPrefix(ktu, keytypeURLPrefix)
}

// KeysetInfoFromPrimitiveSet creates a `KeysetInfo` from a `PrimitiveSet`.
// This function doesn't guarantee to preserve the ordering of the keys in the keyset.
func KeysetInfoFromPrimitiveSet(ps *primitiveset.PrimitiveSet) (*monitoring.KeysetInfo, error) {
	if ps == nil {
		return nil, fmt.Errorf("primitive set is nil")
	}
	if len(ps.Entries) == 0 {
		return nil, fmt.Errorf("primitive set is empty")
	}
	if ps.Primary == nil {
		return nil, fmt.Errorf("primary key must not be nil")
	}
	entries := []*monitoring.Entry{}
	for _, pse := range ps.Entries {
		for _, pe := range pse {
			keyStatus, err := keyStatusFromProto(pe.Status)
			if err != nil {
				return nil, err
			}
			e := &monitoring.Entry{
				KeyID:     pe.KeyID,
				Status:    keyStatus,
				KeyType:   parseKeyTypeURL(pe.TypeURL),
				KeyPrefix: pe.PrefixType.String(),
			}
			entries = append(entries, e)
		}
	}
	return &monitoring.KeysetInfo{
		Annotations:  ps.Annotations,
		PrimaryKeyID: ps.Primary.KeyID,
		Entries:      entries,
	}, nil
}
