const App: React.FC = () => {
  let localAuth: any = {};
  if (localStorage.getItem(LOCAL_STORAGE_AUTH_KEY)) {
    localAuth = JSON.parse(localStorage.getItem(LOCAL_STORAGE_AUTH_KEY)!)
  }
  const [authenticated, setAuthenticated] = useState<boolean>(localAuth.id !== undefined)
  const [userInfo, setUserInfo] = useState<any>(localAuth)
  const [csrf, setCSRF] = useState('')
  const [unrecoverableError, setUnrecoverableError] = useState('')
  const [chatState, dispatch] = useReducer(reducer, initialChatState);
  const [realTimeStatus, setRealTimeStatus] = useState('🔴')
  const [messageQueue, setMessageQueue] = useState<any[]>([]);

  return (
    <CsrfContext.Provider value={csrf}>
      <AuthContext.Provider value={userInfo}>
        {authenticated ? (
          <ChatContext.Provider value={{ state: chatState, dispatch }}>
            <Router>
              <ChatLayout>
                <Routes>
                  <Route path="/" element={<ChatRoomList />} />
                  <Route path="/search" element={<ChatSearch />} />
                  <Route path="/rooms/:id" element={<ChatRoomDetail />} />
                </Routes>
              </ChatLayout>
            </Router>
          </ChatContext.Provider>
        ) : (
          <ChatLogin />
        )}
      </AuthContext.Provider>
    </CsrfContext.Provider>
  );
};

export default App;

const initialChatState = {
  rooms: [],
  roomsById: {},
  messagesByRoomId: {}
};