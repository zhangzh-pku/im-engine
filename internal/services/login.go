package services

import (
	"errors"

	"github.com/zhangzh-pku/im-engine/internal/models"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type ConcreteLoginService struct {
	db *gorm.DB
}

type LoginService interface {
	Registry(request models.LoginRequest) (*models.User, error)
	Login(request models.LoginRequest) (*models.User, error)
}

func NewLoginService(db *gorm.DB) LoginService {
	return &ConcreteLoginService{db: db}
}

func (s *ConcreteLoginService) Registry(request models.LoginRequest) (*models.User, error) {
	var existingUser models.User
	if err := s.db.Where("phone = ?", request.PhoneNumber).First(&existingUser).Error; err == nil {
		return nil, errors.New("phone number already exists")
	}
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(request.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}
	newUser := models.User{
		PhoneNumber: request.PhoneNumber,
		Password:    string(hashedPassword),
	}
	if err := s.db.Create(&newUser).Error; err != nil {
		return nil, err
	}
	return &newUser, nil
}

func (s *ConcreteLoginService) Login(request models.LoginRequest) (*models.User, error) {
	var existingUser models.User
	if err := s.db.Where("phone = ?", request.PhoneNumber).First(&existingUser).Error; err != nil {
		return nil, errors.New("user not found")
	}
	if err := bcrypt.CompareHashAndPassword([]byte(existingUser.Password), []byte(request.Password)); err != nil {
		return nil, errors.New("password incorrect")
	}
	return &existingUser, nil
}
