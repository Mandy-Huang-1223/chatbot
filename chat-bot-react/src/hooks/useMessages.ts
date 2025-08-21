import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getMessages, sendMessage, editMessage } from "../api/messageQuery";

export const useMessages = (chatroomId: string | null) => {
  const [newMessage, setNewMessage] = useState("");
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [isMessageSending, setIsMessageSending] = useState(false);
  const [isImageUploading, setIsImageUploading] = useState(false);
  const [editingMessageId, setEditingMessageId] = useState<string | null>(null);
  const [editText, setEditText] = useState("");

  const {
    data: messages,
    isLoading: isLoadingMessages,
    refetch: refetchMessages,
  } = useQuery({
    queryKey: ["messages", chatroomId],
    queryFn: () => getMessages(chatroomId ?? ""),
    enabled: !!chatroomId,
  });

  const handleImageChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (event.target.files && event.target.files.length > 0) {
      setIsImageUploading(true);
      try {
        await new Promise((resolve) => setTimeout(resolve, 500));
        setSelectedImage(event.target.files[0]);
      } catch (error) {
        console.error("Error processing image:", error);
      } finally {
        setIsImageUploading(false);
      }
    }
  };

  const handleRemoveImage = () => {
    setSelectedImage(null);
  };

  const sendMessageToGemini = async () => {
    setIsMessageSending(true);
    if (newMessage.trim() !== "" || selectedImage) {
      try {
        if (!chatroomId) {
          console.error("No chatroom selected.");
          return;
        }

        await sendMessage(chatroomId, newMessage, selectedImage);

        setNewMessage("");
        setSelectedImage(null);
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        setIsMessageSending(false);
        refetchMessages();
      }
    }
  };

  const startEditingMessage = (messageId: string, currentText: string) => {
    setEditingMessageId(messageId);
    setEditText(currentText);
  };

  const cancelEditingMessage = () => {
    setEditingMessageId(null);
    setEditText("");
  };

  const saveEditedMessage = async () => {
    if (!editingMessageId || !editText.trim()) return;

    try {
      await editMessage(editingMessageId, editText);
      setEditingMessageId(null);
      setEditText("");
      refetchMessages();
    } catch (error) {
      console.error("Error editing message:", error);
    }
  };

  return {
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
    refetchMessages,
  };
};
