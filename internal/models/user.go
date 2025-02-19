package models

type LoginRequest struct {
	PhoneNumber string `json:"phone_number" binding:"required"`
	Password    string `json:"password" binding:"required"`
}

type User struct {
	ID          int    `json:"id" gorm:"primary_key"`
	PhoneNumber string `json:"phone_number" gorm:"unique;not null"`
	Password    string `json:"password" gorm:"not null"`
	FriendIDs   []int  `json:"friend_ids"`
}

type FriendStatus struct {
	UserID   int `json:"user_id" gorm:"primary_key"`
	FriendID int `json:"friend_id" gorm:"primary_key"`
	// 0: pending, 1: accepted, 2: rejected
	Status int `json:"status"`
}
