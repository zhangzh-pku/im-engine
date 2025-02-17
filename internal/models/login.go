package models

type LoginRequest struct {
	PhoneNumber string `json:"phone_number" binding:"required"`
	Password    string `json:"password" binding:"required"`
}

type User struct {
	ID          int    `json:"id" gorm:"primary_key"`
	PhoneNumber string `json:"phone_number" gorm:"unique;not null"`
	Password    string `json:"password" gorm:"not null"`
}
