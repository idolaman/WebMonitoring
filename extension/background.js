// Configuration
const BACKEND_URL = 'http://localhost:8000';
let monitoredDomains = [];

// Initialize extension on install/update
chrome.runtime.onInstalled.addListener(() => {
  console.log('Request Monitor extension installed/updated');
  loadConfiguration();
  setupPeriodicConfigReload();
});

// Initialize extension on startup (when service worker starts)
chrome.runtime.onStartup.addListener(() => {
  console.log('Request Monitor extension starting up');
  loadConfiguration();
  setupPeriodicConfigReload();
});

// Setup periodic configuration reload using Chrome Alarms API
function setupPeriodicConfigReload() {
  chrome.alarms.clear('configReload');

  chrome.alarms.create('configReload', {
    delayInMinutes: 1,
    periodInMinutes: 1
  });
  
  console.log('Periodic config reload scheduled (every 1 minute - minimum allowed)');
}

// Handle alarm events
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'configReload') {
    console.log('Reloading configuration via alarm...');
    loadConfiguration();
  }
});

// Load configuration from backend
async function loadConfiguration() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/config`);
    if (response.ok) {
      const domains = await response.json();
      monitoredDomains = domains || [];
      
      console.log('Configuration loaded:', domains);
      
      setupRequestMonitoring();
    } else {
      console.error('Failed to load configuration:', response.status);
    }
  } catch (error) {
    console.error('Error loading configuration:', error);
  }
}

// Setup request monitoring
function setupRequestMonitoring() {
  // Remove existing listeners
  if (chrome.webRequest.onBeforeSendHeaders.hasListener(handleRequest)) {
    chrome.webRequest.onBeforeSendHeaders.removeListener(handleRequest);
  }
  
  // Add listener for monitored domains
  if (monitoredDomains.length > 0) {
    const urls = monitoredDomains.map(domain => `*://${domain}/*`);
    
    chrome.webRequest.onBeforeSendHeaders.addListener(
      handleRequest,
      { urls: urls },
      ['requestHeaders']
    );
    
    console.log('Monitoring domains:', monitoredDomains);
  }
}

// Handle intercepted requests
function handleRequest(details) {
  // Skip non-main frame requests for now (optional)
  if (details.type !== 'main_frame' && details.type !== 'xmlhttprequest' && details.type !== 'fetch') {
    return;
  }
  
  // Prepare request data
  const requestData = {
    url: details.url,
    method: details.method || 'GET',
    headers: extractHeaders(details.requestHeaders || []),
    timestamp: new Date().toISOString()
  };
  
  // Send to backend
  sendToBackend(requestData);
}

// Extract headers from Chrome's format
function extractHeaders(chromeHeaders) {
  const headers = {};
  chromeHeaders.forEach(header => {
    headers[header.name] = header.value;
  });
  return headers;
}

// Send request data to backend
async function sendToBackend(requestData) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/requests`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Request sent to backend:', requestData.url, result);
    } else {
      console.error('Failed to send request to backend:', response.status);
    }
  } catch (error) {
    console.error('Error sending request to backend:', error);
  }
} 