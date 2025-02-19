package services

import (
	"errors"
	"fmt"
	"sort"

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

func (s *ConcreteUserService) GetUserTable() *gorm.DB {
	return s.db.Table("users")
}

func (s *ConcreteUserService) GetFriendTable() *gorm.DB {
	return s.db.Table("friends")
}

func (s *ConcreteUserService) Registry(request models.LoginRequest) (*models.User, error) {
	var existingUser models.User
	if err := s.GetUserTable().Where("phone = ?", request.PhoneNumber).First(&existingUser).Error; err == nil {
		return nil, errors.New("phone number already exists")
	}
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(request.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}
	newUser := models.User{
		PhoneNumber: request.PhoneNumber,
		Password:    string(hashedPassword),
		FriendIDs:   []int{},
	}
	if err := s.GetUserTable().Create(&newUser).Error; err != nil {
		return nil, err
	}
	return &newUser, nil
}

func (s *ConcreteUserService) Login(request models.LoginRequest) (*models.User, error) {
	var existingUser models.User
	if err := s.GetUserTable().Where("phone = ?", request.PhoneNumber).First(&existingUser).Error; err != nil {
		return nil, errors.New("user not found")
	}
	if err := bcrypt.CompareHashAndPassword([]byte(existingUser.Password), []byte(request.Password)); err != nil {
		return nil, errors.New("password incorrect")
	}
	return &existingUser, nil
}

func (s *ConcreteUserService) SendMessage(sender models.User, receiver models.User, message string) error {
	client := GetMqttClient()
	topic := fmt.Sprintf("chat/dm/%d/%d", sender.ID, receiver.ID)
	client.Publish(topic, message)
	return nil
}

func (s *ConcreteUserService) AddFriend(userID int, friendID int) error {
	var user models.User
	if err := s.GetUserTable().Where("id = ?", userID).First(&user).Error; err != nil {
		return errors.New("user not found")
	}
	var friend models.User
	if err := s.GetUserTable().Where("id = ?", friendID).First(&friend).Error; err != nil {
		return errors.New("friend not found")
	}
	user.FriendIDs = append(user.FriendIDs, friendID)
	friend.FriendIDs = append(friend.FriendIDs, userID)
	// sort
	sort.Ints(user.FriendIDs)
	sort.Ints(friend.FriendIDs)
	// save
	if err := s.GetUserTable().Save(&user).Error; err != nil {
		return err
	}
	if err := s.GetUserTable().Save(&friend).Error; err != nil {
		return err
	}
	// friend status 0: pending 1: accepted 2: rejected
	if err := s.GetFriendTable().Where("user_id = ? AND friend_id = ?", friendID, userID).Update("status", 1).Error; err != nil {
		return err
	}
	return nil
}

func (s *ConcreteUserService) AddFriendRequest(userID int, friendID int) error {
	if err := s.GetFriendTable().Create(&models.FriendStatus{
		UserID:   userID,
		FriendID: friendID,
		Status:   0,
	}).Error; err != nil {
		return err
	}
	return nil
}

func (s *ConcreteUserService) RejectFriendRequest(userID int, friendID int) error {
	if err := s.GetFriendTable().Where("user_id = ? AND friend_id = ?", friendID, userID).Update("status", 1).Error; err != nil {
		return err
	}
	return nil
}

func (s *ConcreteUserService) GetFriendRequests(userID int) ([]models.FriendStatus, error) {
	var friendRequests []models.FriendStatus
	if err := s.GetFriendTable().Where("friend_id = ? AND status = 0", userID).Find(&friendRequests).Error; err != nil {
		return nil, err
	}
	return friendRequests, nil
}

func (s *ConcreteUserService) GetFriends(userID int) ([]models.User, error) {
	var user models.User
	if err := s.GetUserTable().Where("id = ?", userID).First(&user).Error; err != nil {
		return nil, errors.New("user not found")
	}
	var friends []models.User
	if err := s.GetUserTable().Where("id IN ?", user.FriendIDs).Find(&friends).Error; err != nil {
		return nil, err
	}
	return friends, nil
}
