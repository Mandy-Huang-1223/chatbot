import { Box, Tab, Tabs } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import type { ChatRoom } from "../model/chatroom";
import { useState } from "react";

interface ChatroomTabProps {
  activeChatRoom: string;
  handleTabChange: (event: React.SyntheticEvent, newValue: string) => void;
  chatRooms: ChatRoom[];
  handleNewChatRoomOpen: () => void;
  onDeleteChatroom: (chatroomId: string, chatroomName: string) => void;
}

export const ChatroomTab: React.FC<ChatroomTabProps> = ({
  activeChatRoom,
  handleTabChange,
  chatRooms,
  handleNewChatRoomOpen,
  onDeleteChatroom,
}) => {
  const [hoveredTab, setHoveredTab] = useState<string | null>(null);
  const chatRoomNames = chatRooms?.map((room) => room.name);

  const handleMouseEnter = (chatroomName: string) => {
    setHoveredTab(chatroomName);
  };

  const handleMouseLeave = () => {
    setHoveredTab(null);
  };

  const handleDeleteClick = (
    event: React.MouseEvent,
    chatroomId: string,
    chatroomName: string
  ) => {
    event.stopPropagation();
    onDeleteChatroom(chatroomId, chatroomName);
  };

  return (
    <Box sx={{ width: "100%", maxWidth: 800 }}>
      <Tabs
        value={chatRoomNames?.includes(activeChatRoom) ? activeChatRoom : false}
        onChange={handleTabChange}
        aria-label="chat rooms"
      >
        {chatRooms?.map((room) => (
          <Tab
            key={room.name}
            label={
              <Box
                sx={{ display: "flex", alignItems: "center", gap: 1 }}
                onMouseEnter={() => handleMouseEnter(room.name)}
                onMouseLeave={handleMouseLeave}
              >
                {`${room.name} (${room.message_count})`}
                {hoveredTab === room.name && (
                  <CloseIcon
                    fontSize="small"
                    sx={{
                      cursor: "pointer",
                      "&:hover": { color: "error.main" },
                    }}
                    onClick={(event) =>
                      handleDeleteClick(event, room.id, room.name)
                    }
                  />
                )}
              </Box>
            }
            value={room.name}
          />
        ))}
        <Tab
          label={
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              New Chat
              <AddIcon />
            </Box>
          }
          onClick={handleNewChatRoomOpen}
          value="new" 
        />
      </Tabs>
    </Box>
  );
};
