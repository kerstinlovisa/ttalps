#include "SampleAnalyzer/User/Analyzer/ttalp.h"
#include <random>
//#include <math>
using namespace MA5;
using namespace std;


// -----------------------------------------------------------------------------
// Initialize
// function called one time at the beginning of the analysis
// -----------------------------------------------------------------------------
bool ttalp::Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters)
{
    ofstream signaloutput;
    signaloutput.open("../Output/TXT/muon_count.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
    signaloutput.open("../Output/TXT/muon_pair_count.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
    cout << "Initialised Outputfiles" << endl;
    return true;
}

// -----------------------------------------------------------------------------
// Finalize
// function called one time at the end of the analysis
// -----------------------------------------------------------------------------
void ttalp::Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files)
{

}

// -----------------------------------------------------------------------------
// Execute
// function called each time one event is read
// -----------------------------------------------------------------------------
bool ttalp::Execute(SampleFormat& sample, const EventFormat& event)
{
    if (event.mc()!=0)
    {
        int muon_count = 0;
        int muon_pair_count = 0;
        bool top_found = false;
        bool atop_found = false;
        for (MAuint32 i=0;i<event.mc()->particles().size();i++)
        {
        	MCParticleFormat part = event.mc()->particles()[i];
        	if (part.pdgid() == 6)
        	{
        		top_found = true;
        	}
        	else if (part.pdgid() == -6)
        	{
        		atop_found = true;
        	}
            else if (abs(part.pdgid())==13) 
            {
                muon_count ++;
                MCParticleFormat mother = *part.mothers()[0];
                int muon_sisters = 0;
                for (MAuint32 j=0;j<mother.daughters().size();j++)
                {
                    MCParticleFormat sister = *mother.daughters()[j];
                    if (abs(sister.pdgid()) == 13)
                    {
                        muon_sisters++;
                    }
                    if (muon_sisters==2)
                    {
                        muon_pair_count ++;
                    }
                    else if (muon_sisters > 2)
                    {
                        cout << "Found strange number of muon siblings: " << muon_sisters << endl;
                    }
                }
            }
        }
        if (top_found and atop_found)
        {
	        ofstream signaloutput;
	        signaloutput.open("../Output/TXT/muon_count.txt",ios::app);
	        signaloutput << muon_count << endl;
	        signaloutput.close();
	        signaloutput.open("../Output/TXT/muon_pair_count.txt",ios::app);
	        signaloutput << muon_pair_count/2 << endl;
	        signaloutput.close();
	    }
	    else
	    {
	    	cout << "Top and Antitop were not found, event ignored." << endl;
	    }
        return true;
    }
    cout << "no event" << endl;
    return true;
}
