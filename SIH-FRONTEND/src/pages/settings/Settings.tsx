import { useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { User, Bell, Shield, Palette, Database, Info, LogOut } from "lucide-react";

export function Settings() {
  const [activeTab, setActiveTab] = useState("profile");
  const { user } = useAuth();
  const USER_NAME = user ? `${user.first_name || ''} ${user.last_name || ''}`.trim() || "User" : "User";
  const USER_EMAIL = user ? user.sub : "user@odyssey.app";
  const AVATAR_INITIALS = user ? `${(user.first_name || "U")[0]}${(user.last_name || "S")[0]}`.toUpperCase() : "US";

  return (
    <div className="w-full relative">
      <main className="flex-1 w-full max-w-5xl mx-auto p-6 md:p-8 space-y-8 relative z-10">
        
        {/* Page title */}
        <div>
          <h2 className="text-[28px] md:text-[34px] font-bold text-slate-900 tracking-tight">
            Settings
          </h2>
          <p className="text-slate-500 mt-2 text-[15px] max-w-2xl">
            Manage your profile, account and Odyssey preferences.
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          
          {/* Settings Navigation */}
          <div className="w-full md:w-64 shrink-0 space-y-1">
            <button 
              onClick={() => setActiveTab("profile")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'profile' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <User size={18} className={activeTab === 'profile' ? 'text-blue-600' : 'text-slate-400'} /> 
              Profile
            </button>
            <button 
              onClick={() => setActiveTab("security")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'security' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <Shield size={18} className={activeTab === 'security' ? 'text-blue-600' : 'text-slate-400'} /> 
              Account & Security
            </button>
            <button 
              onClick={() => setActiveTab("notifications")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'notifications' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <Bell size={18} className={activeTab === 'notifications' ? 'text-blue-600' : 'text-slate-400'} /> 
              Notifications
            </button>
            <button 
              onClick={() => setActiveTab("appearance")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'appearance' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <Palette size={18} className={activeTab === 'appearance' ? 'text-blue-600' : 'text-slate-400'} /> 
              Appearance
            </button>
            <button 
              onClick={() => setActiveTab("privacy")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'privacy' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <Database size={18} className={activeTab === 'privacy' ? 'text-blue-600' : 'text-slate-400'} /> 
              Privacy & Data
            </button>
            <button 
              onClick={() => setActiveTab("about")}
              className={`w-full text-left px-4 py-2.5 rounded-lg font-medium text-[14px] md:text-[15px] flex items-center gap-3 transition-colors ${activeTab === 'about' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              <Info size={18} className={activeTab === 'about' ? 'text-blue-600' : 'text-slate-400'} /> 
              About
            </button>
          </div>

          {/* Settings Content Area */}
          <div className="flex-1 max-w-3xl">
            
            {/* PROFILE TAB */}
            {activeTab === "profile" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="bg-slate-50 border-b border-slate-100 px-6 py-5">
                  <h3 className="text-[20px] md:text-[24px] font-bold text-slate-800">Profile</h3>
                  <p className="text-[14px] text-slate-500 mt-1">Manage your personal information.</p>
                </div>
                <div className="p-6 md:p-8 space-y-8">
                  
                  {/* Photo */}
                  <div className="flex flex-col sm:flex-row sm:items-center gap-6">
                    <div className="h-24 w-24 rounded-full bg-blue-600 flex items-center justify-center text-white text-3xl font-bold shadow-sm ring-4 ring-slate-50">
                      {AVATAR_INITIALS}
                    </div>
                    <div>
                      <button className="px-5 py-2.5 bg-white border border-slate-300 rounded-xl text-[14px] font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-slate-100">
                        Change photo
                      </button>
                      <p className="text-[13px] text-slate-400 mt-3">JPG, GIF or PNG. 1MB max.</p>
                    </div>
                  </div>

                  {/* Form */}
                  <div className="space-y-5">
                    <div className="space-y-2">
                      <label className="text-[13px] font-semibold text-slate-500 uppercase tracking-wider">Full Name</label>
                      <input type="text" defaultValue={USER_NAME} className="w-full border border-slate-200 rounded-xl px-4 py-3 text-[15px] md:text-[16px] text-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all shadow-sm" />
                    </div>
                    
                    <div className="space-y-2">
                      <label className="text-[13px] font-semibold text-slate-500 uppercase tracking-wider flex items-center justify-between">
                        <span>Email</span>
                        <span className="text-xs text-slate-400 normal-case font-normal">Managed by your account</span>
                      </label>
                      <input type="email" defaultValue={USER_EMAIL} className="w-full border border-slate-200 rounded-xl px-4 py-3 text-[15px] md:text-[16px] text-slate-500 bg-slate-50 cursor-not-allowed outline-none shadow-sm" readOnly />
                    </div>

                    <div className="space-y-2">
                      <label className="text-[13px] font-semibold text-slate-500 uppercase tracking-wider">Phone</label>
                      <input type="tel" defaultValue={""} placeholder="Add phone number..." className="w-full border border-slate-200 rounded-xl px-4 py-3 text-[15px] md:text-[16px] text-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all shadow-sm" />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                      <div className="space-y-2">
                        <label className="text-[13px] font-semibold text-slate-500 uppercase tracking-wider">Organization</label>
                        <input type="text" defaultValue={""} placeholder="Add organization..." className="w-full border border-slate-200 rounded-xl px-4 py-3 text-[15px] md:text-[16px] text-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all shadow-sm" />
                      </div>
                      <div className="space-y-2">
                        <label className="text-[13px] font-semibold text-slate-500 uppercase tracking-wider">Role</label>
                        <input type="text" defaultValue={""} placeholder="Add role..." className="w-full border border-slate-200 rounded-xl px-4 py-3 text-[15px] md:text-[16px] text-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all shadow-sm" />
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 flex justify-end">
                    <button className="px-6 py-3 bg-blue-600 text-white rounded-xl text-[14px] md:text-[15px] font-bold hover:bg-blue-700 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-500/30">
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* ACCOUNT & SECURITY TAB */}
            {activeTab === "security" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="bg-slate-50 border-b border-slate-100 px-6 py-5">
                  <h3 className="text-[20px] md:text-[24px] font-bold text-slate-800">Account & Security</h3>
                  <p className="text-[14px] text-slate-500 mt-1">Manage your password and authentication methods.</p>
                </div>
                <div className="p-6 md:p-8 space-y-8">
                  
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
                    <div>
                      <h4 className="text-[15px] font-bold text-slate-800">Password</h4>
                      <p className="text-[14px] text-slate-500 mt-1">Change the password used to sign in to your account.</p>
                    </div>
                    <button className="px-5 py-2.5 bg-white border border-slate-300 rounded-xl text-[14px] font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-slate-100 shrink-0">
                      Change Password
                    </button>
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
                    <div>
                      <h4 className="text-[15px] font-bold text-slate-800">Two-factor authentication</h4>
                      <p className="text-[14px] text-slate-500 mt-1">Add an extra layer of security to your account.</p>
                    </div>
                    <span className="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-semibold uppercase tracking-wider rounded-lg shrink-0 w-fit">
                      Coming Soon
                    </span>
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-2">
                    <div>
                      <h4 className="text-[15px] font-bold text-rose-600">Sign out</h4>
                      <p className="text-[14px] text-slate-500 mt-1">Sign out of Odyssey on this device.</p>
                    </div>
                    <button className="flex items-center justify-center gap-2 px-5 py-2.5 bg-white border border-rose-200 text-rose-600 rounded-xl text-[14px] font-semibold hover:bg-rose-50 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-rose-100 shrink-0">
                      <LogOut size={16} />
                      Sign Out
                    </button>
                  </div>

                </div>
              </div>
            )}

            {/* NOTIFICATIONS TAB */}
            {activeTab === "notifications" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="bg-slate-50 border-b border-slate-100 px-6 py-5">
                  <h3 className="text-[20px] md:text-[24px] font-bold text-slate-800">Notifications</h3>
                  <p className="text-[14px] text-slate-500 mt-1">Control how Odyssey alerts you about voyage intelligence.</p>
                </div>
                <div className="p-6 md:p-8 space-y-6">
                  
                  {[
                    { title: "Recommendation ready", desc: "Get notified when a voyage recommendation is calculated.", defaultOn: true },
                    { title: "Approval required", desc: "Get notified when a workflow step requires your explicit approval.", defaultOn: true },
                    { title: "Risk alerts", desc: "Receive immediate alerts if voyage risk score becomes elevated.", defaultOn: true },
                    { title: "Voyage updates", desc: "Receive updates regarding market changes impacting active voyages.", defaultOn: true },
                    { title: "System updates", desc: "Important news and updates about Odyssey features.", defaultOn: false },
                  ].map((item) => (
                    <div key={item.title} className="flex items-start justify-between gap-4 pb-6 border-b border-slate-100 last:border-0 last:pb-0">
                      <div>
                        <h4 className="text-[15px] font-semibold text-slate-800">{item.title}</h4>
                        <p className="text-[14px] text-slate-500 mt-0.5">{item.desc}</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer shrink-0 mt-1">
                        <input type="checkbox" className="sr-only peer" defaultChecked={item.defaultOn} />
                        <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-100 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </div>
                  ))}

                </div>
              </div>
            )}

            {/* APPEARANCE TAB */}
            {activeTab === "appearance" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="bg-slate-50 border-b border-slate-100 px-6 py-5">
                  <h3 className="text-[20px] md:text-[24px] font-bold text-slate-800">Appearance</h3>
                  <p className="text-[14px] text-slate-500 mt-1">Customize how Odyssey looks on your device.</p>
                </div>
                <div className="p-6 md:p-8">
                  
                  <div className="space-y-4">
                    <h4 className="text-[15px] font-semibold text-slate-800">Theme</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <label className="cursor-pointer">
                        <input type="radio" name="theme" className="sr-only peer" defaultChecked />
                        <div className="border-2 border-slate-200 rounded-xl p-4 text-center hover:bg-slate-50 peer-checked:border-blue-600 peer-checked:bg-blue-50 transition-all">
                          <div className="h-20 bg-slate-100 rounded-lg mb-3 shadow-inner flex items-center justify-center border border-slate-200">
                            <div className="w-8 h-8 rounded-full bg-white shadow-sm"></div>
                          </div>
                          <span className="text-[14px] font-bold text-slate-700">Light</span>
                        </div>
                      </label>
                      <label className="cursor-pointer opacity-50 relative">
                        <input type="radio" name="theme" className="sr-only peer" disabled />
                        <div className="border-2 border-slate-200 rounded-xl p-4 text-center transition-all bg-slate-50">
                          <div className="h-20 bg-slate-800 rounded-lg mb-3 shadow-inner flex items-center justify-center border border-slate-700">
                            <div className="w-8 h-8 rounded-full bg-slate-900 shadow-sm"></div>
                          </div>
                          <span className="text-[14px] font-bold text-slate-700 flex items-center justify-center gap-1.5">
                            Dark <span className="text-[10px] uppercase tracking-wider bg-slate-200 px-1.5 py-0.5 rounded-md">Soon</span>
                          </span>
                        </div>
                      </label>
                      <label className="cursor-pointer opacity-50 relative">
                        <input type="radio" name="theme" className="sr-only peer" disabled />
                        <div className="border-2 border-slate-200 rounded-xl p-4 text-center transition-all bg-slate-50">
                          <div className="h-20 bg-gradient-to-br from-slate-100 to-slate-800 rounded-lg mb-3 shadow-inner flex items-center justify-center border border-slate-300">
                            <div className="w-8 h-8 rounded-full bg-white/50 backdrop-blur-sm shadow-sm"></div>
                          </div>
                          <span className="text-[14px] font-bold text-slate-700 flex items-center justify-center gap-1.5">
                            System <span className="text-[10px] uppercase tracking-wider bg-slate-200 px-1.5 py-0.5 rounded-md">Soon</span>
                          </span>
                        </div>
                      </label>
                    </div>
                  </div>

                </div>
              </div>
            )}

            {/* PRIVACY & DATA TAB */}
            {activeTab === "privacy" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="bg-slate-50 border-b border-slate-100 px-6 py-5">
                  <h3 className="text-[20px] md:text-[24px] font-bold text-slate-800">Privacy & Data</h3>
                  <p className="text-[14px] text-slate-500 mt-1">Manage your application data and history.</p>
                </div>
                <div className="p-6 md:p-8 space-y-6">
                  
                  <div className="bg-blue-50 text-blue-800 p-4 rounded-xl text-[14px] leading-relaxed border border-blue-100">
                    <strong>Note:</strong> Some demo information and voyage context is currently stored locally on this device.
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
                    <div>
                      <h4 className="text-[15px] font-bold text-slate-800">Voyage History</h4>
                      <p className="text-[14px] text-slate-500 mt-1">View previously evaluated voyage scenarios.</p>
                    </div>
                    <button className="px-5 py-2.5 bg-white border border-slate-300 rounded-xl text-[14px] font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-slate-100 shrink-0">
                      View History
                    </button>
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
                    <div>
                      <h4 className="text-[15px] font-bold text-slate-800">Download My Data</h4>
                      <p className="text-[14px] text-slate-500 mt-1">Export your local configurations and voyage decisions.</p>
                    </div>
                    <button className="px-5 py-2.5 bg-white border border-slate-300 rounded-xl text-[14px] font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-slate-100 shrink-0">
                      Download
                    </button>
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <h4 className="text-[15px] font-bold text-rose-600">Clear Local Data</h4>
                      <p className="text-[14px] text-slate-500 mt-1">Permanently remove all local voyage and evaluation data.</p>
                    </div>
                    <button className="px-5 py-2.5 bg-rose-50 border border-rose-200 rounded-xl text-[14px] font-bold text-rose-700 hover:bg-rose-100 transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-rose-100 shrink-0">
                      Clear Data
                    </button>
                  </div>

                </div>
              </div>
            )}

            {/* ABOUT TAB */}
            {activeTab === "about" && (
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
                <div className="p-8 md:p-12 text-center space-y-6 flex flex-col items-center">
                  <div className="w-20 h-20 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-200">
                    <Database size={36} className="text-white" />
                  </div>
                  <div>
                    <h3 className="text-[24px] font-bold text-slate-900 tracking-tight">About Odyssey</h3>
                    <p className="text-[16px] text-slate-500 mt-2 max-w-md mx-auto leading-relaxed">
                      Smart Shipping Intelligence
                    </p>
                  </div>
                  
                  <div className="inline-block bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 mt-2">
                    <span className="text-[13px] font-bold text-slate-500 uppercase tracking-widest">Version 1.0.0</span>
                  </div>

                  <p className="text-[14px] text-slate-400 mt-8 pt-8 border-t border-slate-100 w-full">
                    SIH 2026
                  </p>
                </div>
              </div>
            )}

          </div>
        </div>

      </main>
    </div>
  );
}




