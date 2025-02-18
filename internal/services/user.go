package services

import (
	"errors"
	"fmt"

	"github.com/zhangzh-pku/im-engine/internal/models"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type ConcreteUserService struct {
	db *gorm.DB
}

type UserService interface {
	Registry(request models.LoginRequest) (*models.User, error)
	Login(request models.LoginRequest) (*models.User, error)
}

func NewUserService(db *gorm.DB) UserService {
	return &ConcreteUserService{db: db}
}

func (s *ConcreteUserService) Registry(request models.LoginRequest) (*models.User, error) {
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

func (s *ConcreteUserService) Login(request models.LoginRequest) (*models.User, error) {
	var existingUser models.User
	if err := s.db.Where("phone = ?", request.PhoneNumber).First(&existingUser).Error; err != nil {
		return nil, errors.New("user not found")
	}
	if err := bcrypt.CompareHashAndPassword([]byte(existingUser.Password), []byte(request.Password)); err != nil {
		return nil, errors.New("password incorrect")
	}
	return &existingUser, nil
}

func (s ConcreteUserService) SendMessage(sender models.User, receiver models.User, message string) error {
	client := GetMqttClient()
	topic := fmt.Sprintf("chat/dm/%d/%d", sender.ID, receiver.ID)
	client.Publish(topic, message)
	return nil
}
