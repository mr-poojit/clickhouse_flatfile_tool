import { useState } from 'react';
import ConnectionForm from './ConnectionForm.jsx'; 
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl font-bold text-center my-6">ClickHouse Connection</h1>
      </header>
      <main className="p-6"> {/* Added padding for better layout */}
        <ConnectionForm /> {/* Add the ConnectionForm component here */}
      </main>
    </div>
  );
}

export default App;
