My IM Engine via golang gin mqtt

# Chat API接口

* [`login`](#login)
* [`api.addUserToThread`](#addUserToThread)
* [`api.changeAdminStatus`](#changeAdminStatus)
* [`api.changeArchivedStatus`](#changeArchivedStatus)
* [`api.changeBlockedStatus`](#changeBlockedStatus)
* [`api.createThread`](#createThread)
* [`api.changeThreadImage`](#changeThreadImage)
* [`api.changeNickname`](#changeNickname)
* [`api.changeThreadColor`](#changeThreadColor)
* [`api.changeThreadEmoji`](#changeThreadEmoji)
* [`api.createPoll`](#createPoll)
* [`api.deleteMessage`](#deleteMessage)
* [`api.deleteThread`](#deleteThread)
* [`api.forwardAttachment`](#forwardAttachment)
* [`api.getAppState`](#getAppState)
* [`api.getCurrentUserID`](#getCurrentUserID)
* [`api.getEmojiUrl`](#getEmojiUrl)
* [`api.getFriendsList`](#getFriendsList)
* [`api.getThreadHistory`](#getThreadHistory)
* [`api.getThreadInfo`](#getThreadInfo)
* [`api.getThreadList`](#getThreadList)
* [`api.getThreadPictures`](#getThreadPictures)
* [`api.getUserID`](#getUserID)
* [`api.getUserInfo`](#getUserInfo)
* [`api.handleMessageRequest`](#handleMessageRequest)
* [`api.listen`](#listen)
* [`api.listenMqtt`](#listenMqtt)
* [`api.logout`](#logout)
* [`api.markAsDelivered`](#markAsDelivered)
* [`api.markAsRead`](#markAsRead)
* [`api.markAsReadAll`](#markAsReadAll)
* [`api.muteThread`](#muteThread)
* [`api.removeUserFromThread`](#removeUserFromThread)
* [`api.resolvePhotoUrl`](#resolvePhotoUrl)
* [`api.searchForThread`](#searchForThread)
* [`api.sendMessage`](#sendMessage)
* [`api.sendTypingIndicator`](#sendTypingIndicator)
* [`api.setMessageReaction`](#setMessageReaction)
* [`api.setOptions`](#setOptions)
* [`api.setTitle`](#setTitle)
* [`api.threadColors`](#threadColors)
* [`api.unsendMessage`](#unsendMessage)


<a name="login"></a>

## POST /api/login
用于用户登录的接口

### Request

```json
{
    "phone_number": "string",
    "password": "string"
}
```

### Response

#### Success(200)
```json
{
    "code": 200,
    "data": {
        "token": "string",
        "expires_in": 3600,
        "refresh_token": "string, 如无特殊说明，每个code=200的请求返回都会带这个字段"
    }
}
```

#### Error(400/401/500)

账号密码错误
```json
{
    "code": 401,
    "message": "string",
    "error_type": "string"
}
```
账号被封禁
```json
{
    "code": 401,
    "message": "string",
    "error_type": "string"
}
```

内部报错（后端bug等）
```json
{
    "code": 500,
    "message": "string",
    "error_type": "string"
}
```

<a name="addUserToThread"></a>

## POST /api/theads/[threadID]/members

将一组人加入到一个thread中

__Arguments__

* `userIDs` 一个userID的列表

## DELETE /api/threads/[threadID]/members

将一组人从一个thread中删除

__Arguments__

* `userIDs` 一个userID的列表

<a name="changeAdminStatus"></a>

## POST /api/thread/[threadID]/admins

将一组人设置成管理员

__Arguments__

* `userIDs` 一个userID的列表

## DELETE /api/thread/[threadID]/admins

将一组人从管理员中移除

__Arguments__

* `userIDs` 一个userID的列表

<a name="changeBlockedStatus"></a>

## POST /api/thread[threadID]/blocks

将一组人在某个thread禁言

__Argunments__

* `userIDs` 一个userID的列表

## DELETE /api/thread[threadID]/blocks

将一组人在某个thread解除禁言

__Argunments__

* `userIDs` 一个userID的列表

<a name="createThread"></a>

## POST /api/thread

创建一个thread

### Requests
```json
{
    "name": "string",
    "userIDs": ["abc","def"]
}
```

### Response
```json
{
    "code": 200,
    "data": {
        "refresh_token": "string",
        "thread_id": "string",
    }
}
```

## GET /api/thread/[threadID]

获取一个thread信息

### Response
```json
{
    "name": "string",
    "participant_IDs": ["一个user ID 列表"],
    "admin_IDs": ["管理员ID 列表"],
    "nick_names": {"一个map":"所有人对这个群的备注，如果没有会返回一个空字典"},
}
```

## GET /api/thread/[thread]/messages

获取历史消息

__parameters__
* `before` 某条message ID之前的消息
* `after` 某条message ID之后的消息
* `limit` 消息数量，默认50

## POST /api/thread/[thread]/messages

发消息

### Request

```json
{
    "type": "text|image|file",
    "content": "string，可以先实现text，其他格式后端第一版暂不实现",
    "reply_to": "Optional[string]",
    "mentions": ["string"],
    "attechments": [{
        "type": "image|file",
        "url": "打算接一个对象存储，阿里云是oss，和s3一个用法",
        "name": "string",
        "size": 1024
    }]
}
```

### Response

```json
{
    "code": 200,
    "data": {
        "messageID": "snowflake algorithm"
    }
}
```
## DELETE /api/thread/[thread]/messages/[messageID]

撤回消息

## POST /api/thread/[thread]/messages/[messsageID]/reaction

添加对于消息的反应

### Request

```json
{
    "emoji": "string"
}
```

## DELETE /api/thread/[thread]/messages/[messsageID]/reaction/[emoji]

删除对于消息的反应



## websocket /api/im/connect

服务端可能推送的所有事件

| 事件类型 | 字段 | 描述 |
| --- | --- | --- |
| `"message"`<br/>一条消息被发送到会话中。 | `attachments` | 消息的附件数组。附件类型多样，详见下方附件表。 |
| | `body` | 刚刚接收到的消息对应的字符串。 |
| | `mentions` | 包含消息中被提及/标记的人的对象，格式为 { id: name } |
| | `messageID` | 表示消息ID的字符串。 |
| | `senderID` | 在threadID会话中发送消息的人的ID。 |
| | `threadID` | 表示消息发送所在会话的threadID。 |
| | `isUnread` | 布尔值，表示消息是否已读。 |
| | `type` | 对于此事件类型，始终为字符串 `"message"`。 |
| `"event"`<br/>会话中发生了一个事件。 | `author` | 执行该事件的人。 |
| | `logMessageBody` | 聊天中显示的字符串。 |
| | `logMessageData` | 与事件相关的数据。 |
| | `logMessageType` | 表示事件类型的字符串（`log:subscribe`、`log:unsubscribe`、`log:thread-name`、`log:thread-color`、`log:thread-icon`、`log:user-nickname`） |
| | `threadID` | 表示消息发送所在会话的threadID。 |
| | `type` | 对于此事件类型，始终为字符串 `"event"`。 |
| `"typ"`<br/>会话中的用户正在输入。 | `from` | 开始/停止输入的用户ID。 |
| | `isTyping` | 布尔值，表示某人是否开始输入。 |
| | `threadID` | 表示用户正在输入的会话的threadID。 |
| | `type` | 对于此事件类型，始终为字符串 `"typ"`。 |
| `"read"`<br/>用户已读取消息。 | `threadID` | 表示消息发送所在会话的threadID。 |
| | `time` | 用户读取消息的时间。 |
| | `type` | 对于此事件类型，始终为字符串 `"read"`。 |
| `"read_receipt"`<br/>会话中的用户已看到API用户发送的消息。 | `reader` | 刚刚读取消息的用户ID。 |
| | `threadID` | 消息被读取的会话。 |
| | `time` | 读者读取消息的时间。 |
| | `type` | 对于此事件类型，始终为字符串 `"read_receipt"`。 |
| `"message_reaction"`<br/>用户对消息发送了反应。 | `messageID` | 消息的ID |
| | `offlineThreadingID` | 离线消息ID |
| | `reaction` | 包含反应表情 |
| | `senderID` | 添加反应的消息作者的ID |
| | `threadID` | 消息发送所在会话的ID |
| | `timestamp` | 发送反应的Unix时间戳（毫秒） |
| | `type` | 对于此事件类型，始终为字符串 `"message_reaction"`。 |
| | `userID` | 发送反应的用户ID |
| `"presence"`<br/>用户好友的在线状态。注意接收此事件类型需要通过 `api.setOptions({ updatePresence: true })` 启用 | `statuses` | 用户的在线状态。`0`表示用户空闲（离开2分钟），`2`表示用户在线（我们不知道1或大于2代表什么...） |
| | `timestamp` | 用户最后在线的时间。 |
| | `type` | 对于此事件类型，始终为字符串 `"presence"`。 |
| | `userID` | 此数据包描述状态的用户ID。 |
| `"message_unsend"`<br/>收到来自会话的消息撤回请求。 | `threadID` | 表示收到撤回消息请求的会话的threadID。 |
| | `senderID` | 在threadID上请求撤回消息的人的ID。 |
| | `messageID` | 表示请求撤回的消息ID的字符串。 |
| | `deletionTimestamp` | 请求发送的时间。 |
| | `type` | 对于此事件类型，始终为字符串 `"message_unsend"`。 |
| `"message_reply"`<br/>回复消息被发送到会话。 | `attachments` | 消息的附件数组。附件类型多样，详见下方附件表。 |
| | `body` | 刚刚接收到的消息对应的字符串。 |
| | `mentions` | 包含消息中被提及/标记的人的对象，格式为 { id: name } |
| | `messageID` | 表示消息ID的字符串。 |
| | `senderID` | 在threadID会话中发送消息的人的ID。 |
| | `threadID` | 表示消息发送所在会话的threadID。 |
| | `isUnread` | 布尔值，表示消息是否已读。 |
| | `type` | 对于此事件类型，始终为字符串 `"message_reply"`。 |
| | `messageReply` | 表示被回复消息的对象。内容与普通的 `"message"` 事件相同。 |

