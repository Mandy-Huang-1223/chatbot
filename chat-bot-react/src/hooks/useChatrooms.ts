import { useState, useCallback, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  createNewChatroom,
  getChatrooms,
  deleteChatroom,
} from "../api/chatroomQuery";
import type { ChatRoom } from "../model/chatroom";

export const useChatrooms = () => {
  const [activeChatRoom, setActiveChatRoom] = useState("Default Chatroom");
  const [chatroomId, setChatroomId] = useState<string | null>(null);
  const [isNewChatRoomDialogOpen, setIsNewChatRoomDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [chatroomToDelete, setChatroomToDelete] = useState<{
    id: string;
    name: string;
  } | null>(null);

  const [localMessageCounts, setLocalMessageCounts] = useState<
    Record<string, number>
  >({});

  const { data: chatRooms, refetch: refetchChatRooms } = useQuery({
    queryKey: ["chatRooms"],
    queryFn: getChatrooms,
  });

  const chatroomsWithUpdatedCounts = useMemo(() => {
    if (!chatRooms) return chatRooms;

    return chatRooms.map((room: ChatRoom) => ({
      ...room,
      message_count: localMessageCounts[room.id] ?? room.message_count,
    }));
  }, [chatRooms, localMessageCounts]);

  const incrementMessageCount = useCallback(
    (chatroomId: string, increment: number = 2) => {
      setLocalMessageCounts((prev) => ({
        ...prev,
        [chatroomId]: (prev[chatroomId] ?? 0) + increment,
      }));
    },
    []
  );

  const syncMessageCounts = useCallback(() => {
    if (chatRooms) {
      const apiCounts: Record<string, number> = {};
      chatRooms.forEach((room: ChatRoom) => {
        apiCounts[room.id] = room.message_count;
      });
      setLocalMessageCounts(apiCounts);
    }
  }, [chatRooms]);

  const handleTabChange = useCallback(
    (_: React.SyntheticEvent, newValue: string) => {
      setActiveChatRoom(newValue);
      const newChatroomid = chatroomsWithUpdatedCounts?.find(
        (room: ChatRoom) => room.name === newValue
      )?.id;
      setChatroomId(newChatroomid || null);
    },
    [chatroomsWithUpdatedCounts]
  );

  const handleNewChatRoomOpen = () => {
    setIsNewChatRoomDialogOpen(true);
  };

  const handleNewChatRoomClose = () => {
    setIsNewChatRoomDialogOpen(false);
  };

  const handleCreateNewChatRoom = (newChatRoomName: string) => {
    if (newChatRoomName.trim() !== "") {
      createNewChatroom(newChatRoomName)
        .then(() => {
          handleNewChatRoomClose();
          refetchChatRooms();
        })
        .catch((error) => {
          console.error("Error creating new chat room:", error);
        });
    }
  };

  const handleDeleteChatroom = (chatroomId: string, chatroomName: string) => {
    setChatroomToDelete({ id: chatroomId, name: chatroomName });
    setDeleteDialogOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (chatroomToDelete) {
      try {
        await deleteChatroom(chatroomToDelete.id);
        refetchChatRooms();
      } catch (error) {
        console.error("Error deleting chat room:", error);
      } finally {
        setDeleteDialogOpen(false);
        setChatroomToDelete(null);
      }
    }
  };

  const handleCancelDelete = () => {
    setDeleteDialogOpen(false);
    setChatroomToDelete(null);
  };

  return {
    activeChatRoom,
    setActiveChatRoom,
    chatroomId,
    setChatroomId,
    chatRooms: chatroomsWithUpdatedCounts,
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
    refetchChatRooms,
  };
};
