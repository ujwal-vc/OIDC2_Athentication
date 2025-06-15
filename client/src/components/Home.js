import React, { useEffect, useState } from 'react';

function Home() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3001/', {
      credentials: 'include',
    })
      .then((res) => res.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const pre = doc.querySelector('pre');
        if (pre) {
          setUser(JSON.parse(pre.textContent));
        }
      });
  }, []);

  const handleLogin = () => {
    window.location.href = 'http://192.168.0.100:3001/login';
  };

  const handleLogout = () => {
    window.location.href = 'http://localhost:3001/logout';
  };

  return (
    <div>
      <h1>Welcome to the Auth0 OIDC App</h1>
      {user ? (
        <div>
          <p>Logged in as {user.userinfo.name}</p>
          <pre>{JSON.stringify(user, null, 2)}</pre>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        // <button onClick={() => window.location.href = '/login'}>Login</button>

        <button onClick={handleLogin}>Login</button>
      )}
    </div>
  );
}

export default Home;
