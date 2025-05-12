import { ConfigProvider } from "antd";
import { AI_BOT } from "../utils/constants";

const AIButton = () => {
  const openChatbot = () => {
    window.dispatchEvent(new CustomEvent("AIButtonClick", { detail: "openAIChatbot" }));
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#8A1D1C",
          controlHeightLG: 52,
        },
      }}
    >
      <button
        style={{
          position: "fixed",
          bottom: "26px",
          right: "16px",
          border: "none",
          background: "orange",
          padding: "10px",
          borderRadius: "60%",
          boxShadow: "0 0 10px rgba(0, 0, 0, 0.8)",
          cursor: "pointer",
        }}
        onClick={openChatbot}
      >
        <img 
          src={AI_BOT}
          alt="AI_BOT"
          style={{ width: "50px", height: "45px" }} 
        />
      </button>
    </ConfigProvider>
  );
};

export default AIButton;
