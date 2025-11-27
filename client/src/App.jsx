import "./App.css";
import ChatInterface from "./features/chat/pages/ChatInterface";

function App() {
  return (
    <>
      <div className="min-h-screen bg-primaryColorLight dark:bg-primaryColorDark">
        <ChatInterface />
      </div>
    </>
  );
}

export default App;
