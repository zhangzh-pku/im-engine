package config

import "os"

type Config struct {
	DatabaseURL  string
	MQTTBroker   string
	MQTTUsername string
	MQTTPassword string
}

func LoadConfig() *Config {
	databaseURL := os.Getenv("DATABASE_URL")
	mqttBroker := os.Getenv("MQTT_BROKER")
	mqttUserName := os.Getenv("MQTT_USERNAME")
	mqttPassword := os.Getenv("MQTT_PASSWORD")
	return &Config{
		DatabaseURL:  databaseURL,
		MQTTBroker:   mqttBroker,
		MQTTUsername: mqttUserName,
		MQTTPassword: mqttPassword,
	}
}
