package services

import (
	"strconv"
	"strings"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/zhangzh-pku/im-engine/config"
	"github.com/zhangzh-pku/im-engine/internal/websocket"
)

type MqttClient struct {
	mqttClient mqtt.Client
}

var mqttClient *MqttClient

func GetMqttClient() MqttClient {
	if mqttClient == nil {
		config := config.LoadConfig()
		opts := mqtt.NewClientOptions().AddBroker(config.MQTTBroker)
		opts.SetUsername(config.MQTTUsername)
		opts.SetPassword(config.MQTTPassword)
		opts.SetClientID("im-engine")
		mqttClient = &MqttClient{mqtt.NewClient(opts)}
	}
	return *mqttClient
}

func MessageHandler(client mqtt.Client, msg mqtt.Message) {
	topic := msg.Topic()
	payload := string(msg.Payload())
	if topic[:8] == "chat/dm/" {
		receiver := topic[strings.Index(topic, "_")+1:]
		receiverID, err := strconv.Atoi(receiver)
		if err != nil {
			panic(err)
		}
		wsManager := websocket.GetWebsocketManager()
		if conn, ok := wsManager.Clients[receiverID]; ok {
			conn.WriteMessage(1, []byte(payload))
		}
	}
}

func (mc *MqttClient) Subscribe(topic string) {
	if token := mc.mqttClient.Subscribe(topic, 0, MessageHandler); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
}

func (mc *MqttClient) Publish(topic string, payload string) {
	if token := mc.mqttClient.Publish(topic, 0, false, payload); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
}
