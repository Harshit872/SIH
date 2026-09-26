import re

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Add the Global Action Footer back before </main>
footer = '''
        {/* Global Action Footer */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Proceed to Decision Workspace</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              Move to the Decision Workspace to evaluate costs, risks, and recommended actions based on this forecast.
            </p>
          </div>
          <Button 
            size="lg" 
            onClick={() => {
              markStepComplete('/forecasting');
              navigate('/decision-workspace');
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white w-full md:w-auto shrink-0 shadow-md"
          >
            Go to Decision Workspace
          </Button>
        </div>
'''

text = text.replace('      </main>', footer + '\n      </main>')

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
