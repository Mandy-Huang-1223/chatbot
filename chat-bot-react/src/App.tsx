import React, { useEffect } from "react";
import { Box, Typography } from "@mui/material";
import { ChatInput } from "./components/ChatInput";
import { NewChatroomDialogue } from "./components/NewChatroomDialogue";
import { ChatroomTab } from "./components/ChatroomTab";
import { DeleteConfirmationDialog } from "./components/DeleteConfirmationDialog";
import { MessageList } from "./components/MessageList";
import { useChatrooms } from "./hooks/useChatrooms";
import { useMessages } from "./hooks/useMessages";
import { useScrollToBottom } from "./hooks/useScrollToBottom";

function App() {
  const {
    activeChatRoom,
    setActiveChatRoom,
    chatroomId,
    setChatroomId,
    chatRooms,
    isNewChatRoomDialogOpen,
    deleteDialogOpen,
    chatroomToDelete,
    handleTabChange,
    handleNewChatRoomOpen,
    handleNewChatRoomClose,
    handleCreateNewChatRoom,
    handleDeleteChatroom,
    handleConfirmDelete,
    handleCancelDelete,
    incrementMessageCount,
    syncMessageCounts,
  } = useChatrooms();

  const {
    newMessage,
    setNewMessage,
    selectedImage,
    isMessageSending,
    isImageUploading,
    messages,
    isLoadingMessages,
    editingMessageId,
    editText,
    setEditText,
    handleImageChange,
    handleRemoveImage,
    sendMessageToGemini,
    startEditingMessage,
    cancelEditingMessage,
    saveEditedMessage,
  } = useMessages(chatroomId);

  const { messagesEndRef, scrollToBottom } = useScrollToBottom();

  const sendMessageWithScroll = async () => {
    if (chatroomId) {
      incrementMessageCount(chatroomId, 2);
    }
    await sendMessageToGemini();
    setTimeout(() => scrollToBottom(), 100);
  };

  const handleTabChangeWithScroll = (
    event: React.SyntheticEvent,
    newValue: string
  ) => {
    handleTabChange(event, newValue);
    setTimeout(() => scrollToBottom(), 100);
  };

  useEffect(() => {
    if (chatRooms && chatRooms.length > 0 && !chatroomId) {
      setChatroomId(chatRooms[0].id || null);
      setActiveChatRoom(chatRooms[0].name);
    }
  }, [chatRooms, chatroomId, setChatroomId, setActiveChatRoom]);

  useEffect(() => {
    syncMessageCounts();
  }, [syncMessageCounts]);

  useEffect(() => {
    setTimeout(() => scrollToBottom(), 100);
  }, [messages, scrollToBottom]);

  return (
    <Box
      sx={{
        width: "100%",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Typography variant="h4" component="h1" gutterBottom>
        聊天機器人
      </Typography>

      <>
        <ChatroomTab
          activeChatRoom={activeChatRoom}
          handleTabChange={handleTabChangeWithScroll}
          chatRooms={chatRooms ?? []}
          handleNewChatRoomOpen={handleNewChatRoomOpen}
          onDeleteChatroom={handleDeleteChatroom}
        />

        <MessageList
          messages={messages}
          isLoadingMessages={isLoadingMessages}
          messagesEndRef={messagesEndRef}
          editingMessageId={editingMessageId}
          editText={editText}
          setEditText={setEditText}
          startEditingMessage={startEditingMessage}
          cancelEditingMessage={cancelEditingMessage}
          saveEditedMessage={saveEditedMessage}
        />

        <ChatInput
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          sendMessage={sendMessageWithScroll}
          handleImageChange={handleImageChange}
          isMessageSending={isMessageSending}
          isImageUploading={isImageUploading}
          selectedImage={selectedImage}
          onRemoveImage={handleRemoveImage}
        />
      </>

      <NewChatroomDialogue
        isNewChatRoomDialogOpen={isNewChatRoomDialogOpen}
        handleNewChatRoomClose={handleNewChatRoomClose}
        handleCreateNewChatRoom={handleCreateNewChatRoom}
      />

      <DeleteConfirmationDialog
        open={deleteDialogOpen}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        chatroomName={chatroomToDelete?.name}
      />
    </Box>
  );
}

export default App;
