package models

import (
	"github.com/lib/pq"
)

// Use PostgreSQL native array type for consistency with domain entities
type StringArray = pq.StringArray
