import { useState } from 'react';
import axios from 'axios';  

const ConnectionForm = () => {
  const [formData, setFormData] = useState({
    host: '',
    port: '',
    username: '',
    jwt_token: '',
    database: '',
  });

  const [errors, setErrors] = useState({
    host: '',
    port: '',
    username: '',
    jwt_token: '',
    database: '',
  });

  const [connectionStatus, setConnectionStatus] = useState(null);  // To track the connection status

  // Validate form data
  const validateForm = () => {
    let isValid = true;
    let newErrors = { host: '', port: '', username: '', jwt_token: '', database: '' };

    if (!formData.host) {
      newErrors.host = 'Host is required';
      isValid = false;
    }
    if (!formData.port) {
      newErrors.port = 'Port is required';
      isValid = false;
    }
    if (!formData.username) {
      newErrors.username = 'Username is required';
      isValid = false;
    }
    if (!formData.jwt_token) {
      newErrors.jwt_token = ' Token is required';
      isValid = false;
    }
    if (!formData.database) {
      newErrors.database = ' Database is required';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!validateForm()) {
      return;
    }
  
    try {
      const response = await axios.post('http://localhost:8000/api/connect-clickhouse', formData, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (response.status === 200) {
        setConnectionStatus('Connected successfully!');
      } else {
        setConnectionStatus('Failed to connect!');
      }
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('Error connecting to the server:', error);
      setConnectionStatus('Error connecting to the server!');
    }
  };

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="connection-form">
      <h2 className="text-xl font-bold mb-4">Connect to ClickHouse</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="host" className="block">Host</label>
          <input
            type="text"
            id="host"
            name="host"
            value={formData.host}
            onChange={handleChange}
            className="border p-2 w-full"
          />
          {errors.host && <p className="text-red-500">{errors.host}</p>}
        </div>

        <div className="mb-4">
          <label htmlFor="port" className="block">Port</label>
          <input
            type="text"
            id="port"
            name="port"
            value={formData.port}
            onChange={handleChange}
            className="border p-2 w-full"
          />
          {errors.port && <p className="text-red-500">{errors.port}</p>}
        </div>

        <div className="mb-4">
          <label htmlFor="username" className="block">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="border p-2 w-full"
          />
          {errors.username && <p className="text-red-500">{errors.username}</p>}
        </div>

        <div className="mb-4">
          <label htmlFor="jwt_token" className="block">jwt_token</label>
          <input
            type="jwt_token"
            id="jwt_token"
            name="jwt_token"
            value={formData.jwt_token}
            onChange={handleChange}
            className="border p-2 w-full"
          />
          {errors.jwt_token && <p className="text-red-500">{errors.jwt_token}</p>}
        </div>

        <div className="mb-5">
          <label htmlFor="database" className="block">database</label>
          <input
            type="database"
            id="database"
            name="database"
            value={formData.database}
            onChange={handleChange}
            className="border p-2 w-full"
          />
          {errors.database && <p className="text-red-500">{errors.database}</p>}
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          Connect
        </button>
      </form>

      {connectionStatus && (
        <div className="mt-4 text-center">
          <p>{connectionStatus}</p>
        </div>
      )}
    </div>
  );
};

export default ConnectionForm;
