#include "SampleAnalyzer/User/Analyzer/ALPanalysis.h"
#include <random>
#include <string>
#include <sstream>
#include <cmath>
#include <iterator>
using namespace MA5;
using namespace std;

// -----------------------------------------------------------------------------
// Initialize
// function called one time at the beginning of the analysis
// -----------------------------------------------------------------------------
bool ALPanalysis::Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters)
{
    ofstream signaloutput;
	signaloutput.open("../Output/TXT/muon_count_tot.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
	signaloutput.open("../Output/TXT/muon_count_notop.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
    signaloutput.open("../Output/ttj_bkg/muon_pair_count.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
	signaloutput.open("../Output/TXT/top_count.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
    signaloutput.open("../Output/TXT/muon_data.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
	signaloutput.open("../Output/TXT/muon_pair_ancestor_data.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
	signaloutput.open("../Output/TXT/muon_nonpair_ancestor_data.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();
	signaloutput.open("../Output/TXT/muon_single_ancestor_data.txt",ios::trunc);
    signaloutput << "";
    signaloutput.close();

    cout << "Initialised Outputfiles" << endl;
    return true;
}

// -----------------------------------------------------------------------------
// Finalize
// function called one time at the end of the analysis
// -----------------------------------------------------------------------------
void ALPanalysis::Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files)
{

}

// -----------------------------------------------------------------------------
// Execute
// function called each time one event is read
// -----------------------------------------------------------------------------
bool ALPanalysis::Execute(SampleFormat& sample, const EventFormat& event)
{
    if (event.mc()!=0)
    {

		int top_count = 0;
		int atop_count = 0;
        int muon_count = 0;
        int muon_count_tot = 0;
        int muon_count_notop = 0;
        int muon_pair_count = 0;
        bool top_found = false;
        bool atop_found = false;
        std::string tab = "\t";
        std::string signifier = "|";
        std::string top_data = "";
        std::string atop_data = "";
        std::string muon_pair_data = "";
        std::string muon_nonpair_data = "";
        std::string muon_sister_data = "";
        int muon_sisters = 0;

		std::string muon_pair_ancestors = "";
		std::string muon_nonpair_ancestors = "";
		std::string amuon_nonpair_ancestors = "";

        for (MAuint32 i=0;i<event.mc()->particles().size();i++)
        {
        	MCParticleFormat part = event.mc()->particles()[i];
        	if (part.pdgid() == 6)
        	{
        		top_found = true;
        		top_data += this->data(part);
				top_count += 1;
        	}
        	else if (part.pdgid() == -6)
        	{
        		atop_found = true;
        		atop_data += this->data(part);
				atop_count += 1;
        	}
            // else if (abs(part.pdgid())==13 and not hasTopAncestor(part))
            else if (abs(part.pdgid())==13)
            {
				muon_count_tot += 1;
				if (!hasTopAncestor(part))
				{
					muon_count_notop += 1;
					if (part.statuscode()==1)
					{
						MCParticleFormat mother = *part.mothers()[0];
						MCParticleFormat muon_sister;
						muon_sisters = 1;
						muon_sister_data = "";
						for (MAuint32 j=0;j<mother.daughters().size();j++)
						{
							MCParticleFormat sister = *mother.daughters()[j];
							if ((abs(sister.pdgid()) == 13) && (!(this->data(sister) == this->data(part))))
							{
								muon_sisters++;
								muon_sister_data = this->data(sister);
								muon_sister = sister;
							}
						}
						if (muon_sisters == 1)
						{
							muon_nonpair_data += this->data(part);
							muon_count++;

							std::vector<MCParticleFormat> line;
							line = findAncestorLine(part,line);
							// line.erase(line.begin());
							if (part.pdgid() == 13)
							{
								for (int i = 0; i<line.size(); i++)
								{
									muon_nonpair_ancestors += this->data(line[i]);
								}
							}
							else 
							{
								for (int i = 0; i<line.size(); i++)
								{
									amuon_nonpair_ancestors += this->data(line[i]);
								}
							}
						}
						else if (muon_sisters==2)
						{
							std::string tmp = this->data(part);
							if ((tmp[0]=='-') && (!(muon_sister_data[0]=='-')))
							{
								tmp += muon_sister_data;
							}
							else if ((!(tmp[0]=='-')) && (muon_sister_data[0]=='-'))
							{
								tmp = muon_sister_data + tmp;
								// tmp += muon_sister_data; # This is wrong, keeping it to remember bug
							}
							else
							{
								std::cout << "There are two muons with the same sign that are siblings." << endl;
								muon_nonpair_data += tmp;
								muon_count++;
								continue;
							}
							if ((muon_pair_data.length() < tmp.length()) || (!(0 == muon_pair_data.compare(muon_pair_data.length()-tmp.length(), tmp.length(), tmp))))
							{
								muon_pair_data += tmp;
								muon_pair_count ++;
								muon_count++;
								muon_count++;

								std::vector<MCParticleFormat> line;
								line = findAncestorLine(part,line);
								line.erase(line.begin());
								muon_pair_ancestors += tmp;
								for (int i = 0; i<line.size(); i++)
								{
									muon_pair_ancestors += this->data(line[i]);
								}
							}
						}
						else if (muon_sisters > 2)
						{
							std::cout << "Found strange number of muon siblings: " << muon_sisters << endl;
						}
					}
				}
			} 
        }
        if (top_found && atop_found)
        {
	        std::ofstream signaloutput;
			signaloutput.open("../Output/TXT/top_count.txt",ios::app);
	        signaloutput << top_count << tab << atop_count << endl;
	        signaloutput.close();
			if (muon_count_tot>=2)
			{
				signaloutput.open("../Output/TXT/muon_count_tot.txt",ios::app);
				signaloutput << muon_count_tot << endl;
				signaloutput.close();
			}
			if (muon_count_notop>=2)
			{
				signaloutput.open("../Output/TXT/muon_count_notop.txt",ios::app);
				signaloutput << muon_count_notop << endl;
				signaloutput.close();
				
				signaloutput.open("../Output/TXT/muon_data.txt",ios::app);
				signaloutput << top_data << signifier << tab;
				signaloutput << atop_data << signifier << tab;
				signaloutput << muon_pair_data << signifier << tab;
				signaloutput << muon_nonpair_data << tab;
				signaloutput << muon_pair_ancestors << tab;
				signaloutput << muon_nonpair_ancestors << endl;
				signaloutput.close();
				if (muon_pair_count>0)
				{
					signaloutput.open("../Output/TXT/muon_pair_ancestor_data.txt",ios::app);
					signaloutput << muon_pair_ancestors << endl;
					signaloutput.close();
					signaloutput.open("../Output/TXT/muon_pair_count.txt",ios::app);
					signaloutput << muon_pair_count << endl;
					signaloutput.close();
				}
				else
				{
					signaloutput.open("../Output/TXT/muon_nonpair_ancestor_data.txt",ios::app);
					signaloutput << muon_nonpair_ancestors << signifier << tab;
					signaloutput << amuon_nonpair_ancestors << endl;
					signaloutput.close();
				}
			}
			if (muon_count == 1)
			{
				signaloutput.open("../Output/TXT/muon_single_ancestor_data.txt",ios::app);
				signaloutput << muon_nonpair_ancestors << amuon_nonpair_ancestors << endl;
				signaloutput.close();
			}
	    }
	    else
	    {
	    	std::cout << "Top and Antitop were not found, event ignored." << endl;
	    }
        return true;
    }
    std::cout << "no event" << endl;
    return true;
}

string ALPanalysis::data(MCParticleFormat part)
{
	std::string tab = "\t";
	std::ostringstream ss;
	ss << part.pdgid() << tab;
	ss << part.decay_vertex().T() << tab;
	ss << part.decay_vertex().X() << tab;
	ss << part.decay_vertex().Y() << tab;
	ss << part.decay_vertex().Z() << tab;
	ss << part.e() << tab;
	ss << part.px() << tab;
	ss << part.py() << tab;
	ss << part.pz() << tab;
	std::string result(ss.str());
	return result;
}

bool ALPanalysis::hasTopAncestor(MCParticleFormat part)
{
	if (abs(part.pdgid()) == 6 && part.statuscode()>=60)
	{
		return true;
	}
	if (part.mothers().size()==0)
	{
		return false;
	}
	for (int i=0; i<part.mothers().size(); i++)
	{
		MCParticleFormat mother = *part.mothers()[i];
		if (hasTopAncestor(mother))
		{
			return true;
		}
	}
	return false;
}


std::vector<MCParticleFormat> ALPanalysis::findAncestorLine(MCParticleFormat part, std::vector<MCParticleFormat> line)
{
	if (part.mothers().size() == 0 || abs(part.pdgid()) < 5 || abs(part.pdgid()) == 21)
	{
		return line;
	}
	int id = part.pdgid();
	bool idincluded = false;
	for (int i=0; i < line.size(); i++)
	{
		if (line[i].pdgid() == id) {idincluded=true;}
	}
	if (!idincluded)
	{ 
		line.push_back(part);
	}
	for (int j = 0; j < part.mothers().size(); j++)
	{
		line = findAncestorLine(*part.mothers()[j], line);
	}
	return line;
}


void ALPanalysis::buildOutput (MCParticleFormat &mother, int &n, int &count, std::string &tobebuilt)
{
  count++;
//   int id = abs(mother.pdgid());
//   if (id == 6 || id == 13 || id == 21 || id == 24 || id == 5)
  // if (id == 6 || id == 13 || id == 21 || id == 24 || id == 5 || id == 11)
//   {
  tobebuilt += std::to_string(mother.pdgid())+"\t";
//   }
//   else
//   {
//   	tobebuilt += "\t";
//   }
  n++;
  for(MAuint32 i=0; i<mother.daughters().size(); i++)
	{
	MCParticleFormat dau = *mother.daughters()[i];
	buildOutput(dau, n, count, tobebuilt);
	if(i+1<mother.daughters().size()){
		tobebuilt += "\n";
		for (int j=0; j<n; j++)
		{
			tobebuilt +="\t";
		}
	}
  }
  n--;
}
