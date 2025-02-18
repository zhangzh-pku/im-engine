package websocket

import "github.com/gorilla/websocket"

type WebsocketManager struct {
	Clients    map[int]*websocket.Conn
	Broadcasts map[int]chan string
}

var websocketManager *WebsocketManager

func GetWebsocketManager() *WebsocketManager {
	if websocketManager != nil {
		return websocketManager
	}
	return &WebsocketManager{
		Clients:    make(map[int]*websocket.Conn),
		Broadcasts: make(map[int]chan string),
	}
}

func (m *WebsocketManager) RegisterClient(userID int, conn *websocket.Conn) {
	m.Clients[userID] = conn
	m.Broadcasts[userID] = make(chan string)
}
