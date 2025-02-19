package services

import (
	"sort"

	"github.com/zhangzh-pku/im-engine/internal/models"
	"gorm.io/gorm"
)

type ConcreteThreadService struct {
	db *gorm.DB
}

type ThreadService interface {
}

func NewThreadService(db *gorm.DB) ThreadService {
	return &ConcreteThreadService{db: db}
}

func (s *ConcreteThreadService) GetThreadTable() *gorm.DB {
	return s.db.Table("threads")
}

func (s *ConcreteThreadService) GetThreadMembersTable() *gorm.DB {
	return s.db.Table("thread_members")
}

func (s *ConcreteThreadService) CreateThread(thread models.Thread) (*models.Thread, error) {
	if err := s.GetThreadTable().Create(&thread).Error; err != nil {
		return nil, err
	}
	threadMembers := models.ThreadMembers{
		ThreadID: thread.ID,
		UserID:   thread.OwnerID,
		Role:     "owner",
	}
	if err := s.GetThreadMembersTable().Create(&threadMembers).Error; err != nil {
		return nil, err
	}
	return &thread, nil
}

func (s *ConcreteThreadService) GetThreadByID(threadID int) (*models.Thread, error) {
	var thread models.Thread
	if err := s.GetThreadTable().Where("id = ?", threadID).First(&thread).Error; err != nil {
		return nil, err
	}
	return &thread, nil
}

func (s *ConcreteThreadService) AddMemberToThread(threadID int, userID int) error {
	threadMembers := models.ThreadMembers{
		ThreadID: threadID,
		UserID:   userID,
		Role:     "member",
	}
	var thread models.Thread
	if err := s.GetThreadTable().Where("id = ?", threadID).First(&thread).Error; err != nil {
		return err
	}
	thread.ThreadMembers = append(thread.ThreadMembers, userID)
	sort.Ints(thread.ThreadMembers)
	if err := s.GetThreadTable().Save(&thread).Error; err != nil {
		return nil
	}
	if err := s.GetThreadMembersTable().Create(&threadMembers).Error; err != nil {
		return err
	}
	return nil
}

func (s *ConcreteThreadService) DeleteMemberFromThread(threadID int, userID int) error {
	var thread models.Thread
	if err := s.GetThreadTable().Where("id = ?", threadID).First(&thread).Error; err != nil {
		return err
	}
	for i, member := range thread.ThreadMembers {
		if member == userID {
			thread.ThreadMembers = append(thread.ThreadMembers[:i], thread.ThreadMembers[i+1:]...)
			break
		}
	}
	if err := s.GetThreadTable().Save(&thread).Error; err != nil {
		return err
	}
	if err := s.GetThreadMembersTable().Where("thread_id = ? AND user_id = ?", threadID, userID).Delete(&models.ThreadMembers{}).Error; err != nil {
		return err
	}
	return nil
}
