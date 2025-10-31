import React, { useState, useContext } from 'react';
import logo from './assets/centrifugo.svg'
import CsrfContext from './CsrfContext';
import { login } from './AppApi';

interface ChatLoginProps {
  onSuccess: (userId: string) => void;
}

const ChatLogin: React.FC<ChatLoginProps> = ({ onSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const csrf = useContext(CsrfContext);

  const handleLogin = async () => {
    try {
      const resp = await login(csrf, username, password)
      onSuccess(resp.user.id.toString());
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <form id="chat-login" onSubmit={(e) => {
      e.preventDefault()
      handleLogin()
    }}>
      <div id="chat-login-logo-container">
        <img src={logo} width="100px" height="100px" />
      </div>
      <div className="input-container">
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
      </div>
      <div className="input-container">
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      </div>
      <div className='login-button-container'>
        <button>Login</button>
      </div>
    </form>
  );
};

export default ChatLogin;