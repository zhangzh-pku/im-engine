package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"github.com/zhangzh-pku/im-engine/config"
	"github.com/zhangzh-pku/im-engine/internal/handlers"
	"github.com/zhangzh-pku/im-engine/internal/services"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func main() {
	r := gin.Default()
	cfg := config.LoadConfig()
	dsn := cfg.DatabaseURL
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	UserService := services.NewUserService(db)
	UserHandler := handlers.NewUserHandler(UserService)
	r.POST("/registry", UserHandler.Registry)
	r.POST("/login", UserHandler.Login)

	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run server: %v", err)
	}
}
