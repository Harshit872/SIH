// Demo mode: no backend required. Auth is fully simulated client-side.
// Any email/password or demo access works. A signed-looking JWT is generated locally.

function makeFakeJwt(payload: Record<string, any>): string {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = btoa(JSON.stringify(payload));
  const sig = btoa("demo-signature");
  return `${header}.${body}.${sig}`;
}

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export const authService = {
  async login(email: string, _password: string) {
    await sleep(600); // feels real
    const namePart = email.split("@")[0] || "user";
    const [first, ...rest] = namePart.replace(/[._-]/g, " ").split(" ");
    const payload = {
      sub: email,
      first_name: first || "User",
      last_name: rest.join(" ") || "",
      email,
      exp: Math.floor(Date.now() / 1000) + 60 * 60 * 8, // 8 hours
    };
    return { access_token: makeFakeJwt(payload) };
  },

  async signup(data: {
    first_name: string;
    last_name: string;
    company: string;
    email: string;
    password: string;
  }) {
    await sleep(800); // feels real
    const payload = {
      sub: data.email,
      first_name: data.first_name,
      last_name: data.last_name,
      company: data.company,
      email: data.email,
      exp: Math.floor(Date.now() / 1000) + 60 * 60 * 8,
    };
    return { access_token: makeFakeJwt(payload) };
  },

  getDemoToken() {
    const payload = {
      sub: "demo@odyssey.ai",
      first_name: "Demo",
      last_name: "User",
      email: "demo@odyssey.ai",
      exp: Math.floor(Date.now() / 1000) + 60 * 60 * 8,
    };
    return makeFakeJwt(payload);
  },
};
