package models

type Thread struct {
	ID            int    `json:"id" gorm:"primary_key"`
	OwnerID       int    `json:"owner_id" gorm:"not null"`
	Name          string `json:"name" gorm:"not null"`
	ThreadMembers []int  `json:"thread_members"`
}

type ThreadMembers struct {
	ThreadID int `json:"thread_id" gorm:"primary_key"`
	UserID   int `json:"user_id" gorm:"primary_key"`
	// Role can be "member" or "admin" or "owner"
	Role string `json:"role" gorm:"not null"`
}
