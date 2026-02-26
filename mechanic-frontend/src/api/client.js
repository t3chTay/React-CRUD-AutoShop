const API = import.meta.env.VITE_API_BASE_URL;
console.log("API BASE URL:", API);

export async function apiFetch(path, { token, ...options } = {}) {
  if (!API) throw new Error("VITE_API_BASE_URL is missing. Check mechanic-frontend/.env and restart dev server.");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, { ...options, headers });

  let data = null;
  const text = await res.text();
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!res.ok) {
    const message =
      (data && (data.error || data.message || JSON.stringify(data))) ||
      `Request failed (${res.status})`;
    throw new Error(message);
  }

  return data;
}