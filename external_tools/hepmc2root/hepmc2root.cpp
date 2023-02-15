#include <string>
#include <regex>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <TFile.h>
#include <TTree.h>

using namespace std;

string TREENAME= "Events";
int MAXPART = 5000;
int debug = 0;
int n_daughters = 20;

struct Bag {
  int    Event_numberP;
  int    Event_processID;
  int    Event_number;
  int    Event_numberMP;
  float Event_scale;
  float Event_alphaQCD;
  float Event_alphaQED;
  int    Event_barcodeSPV;
  int    Event_numberV;
  int    Event_barcodeBP1;
  int    Event_barcodeBP2;
  
  
  float Xsection_value;
  float Xsection_error;
  
  int    PDF_parton1;
  int    PDF_parton2;
  float PDF_x1;
  float PDF_x2;
  float PDF_Q2;
  float PDF_x1f;
  float PDF_x2f;
  int    PDF_id1;
  int    PDF_id2;
  
  float Particle_x[5000];
  float Particle_y[5000];
  float Particle_z[5000];
  float Particle_ctau[5000];
  
  int    Particle_barcode[5000];
  int    Particle_pid[5000];
  float Particle_px[5000];
  float Particle_py[5000];
  float Particle_pz[5000];
  float Particle_energy[5000];
  float Particle_mass[5000];
  int    Particle_status[5000];
  int    Particle_d[100][5000];
};

string makeBranchName(string input, string type="F")
{
  return (input+"[Event_numberP]/"+type).c_str();
}

class hepmc2root
{
public:
  hepmc2root(string filename, string outfilename = "", string treename="Events", int complevel=2){
    inp = ifstream(filename);
    
    // get rid of the header
    string line;
    std::getline(inp, line);
    std::getline(inp, line);
    
    file = new TFile(outfilename.c_str(), "recreate");
    tree = new TTree(treename.c_str(), "HEPMC_tree");
    
    bag = Bag();
    
    tree->Branch("Event_numberP", &(bag.Event_numberP), "Event_numberP/I");
    tree->Branch("Event_processID", &(bag.Event_processID), "Event_processID/I");
    tree->Branch("Event_number", &(bag.Event_number), "Event_number/I");
    tree->Branch("Event_numberMP", &(bag.Event_numberMP), "Event_numberMP/I");
    tree->Branch("Event_scale", &(bag.Event_scale), "Event_scale/F");
    tree->Branch("Event_alphaQCD", &(bag.Event_alphaQCD), "Event_alphaQCD/F");
    tree->Branch("Event_alphaQED", &(bag.Event_alphaQED), "Event_alphaQED/F");
    tree->Branch("Event_barcodeSPV", &(bag.Event_barcodeSPV), "Event_barcodeSPV/I");
    tree->Branch("Event_numberV", &(bag.Event_numberV), "Event_numberV/I");
    tree->Branch("Event_barcodeBP1", &(bag.Event_barcodeBP1), "Event_barcodeBP1/I");
    tree->Branch("Event_barcodeBP2", &(bag.Event_barcodeBP2), "Event_barcodeBP2/I");
    
    tree->Branch("Xsection_value", &(bag.Xsection_value), "Xsection_value/F");
    tree->Branch("Xsection_error", &(bag.Xsection_error), "Xsection_error/F");
    
    tree->Branch("PDF_parton1", &(bag.PDF_parton1), "PDF_parton1/I");
    tree->Branch("PDF_parton2", &(bag.PDF_parton2), "PDF_parton2/I");
    tree->Branch("PDF_x1", &(bag.PDF_x1), "PDF_x1/F");
    tree->Branch("PDF_x2", &(bag.PDF_x2), "PDF_x2/F");
    tree->Branch("PDF_Q2", &(bag.PDF_Q2), "PDF_Q2/F");
    tree->Branch("PDF_x1f", &(bag.PDF_x1f), "PDF_x1f/F");
    tree->Branch("PDF_x2f", &(bag.PDF_x2f), "PDF_x2f/F");
    tree->Branch("PDF_id1", &(bag.PDF_id1), "PDF_id1/I");
    tree->Branch("PDF_id2", &(bag.PDF_id2), "PDF_id2/I");
    
    tree->Branch("Particle_x", &(bag.Particle_x), makeBranchName("Particle_x", "F").c_str());
    tree->Branch("Particle_y", &(bag.Particle_y), makeBranchName("Particle_y", "F").c_str());
    tree->Branch("Particle_z", &(bag.Particle_z), makeBranchName("Particle_z", "F").c_str());
    
    tree->Branch("Particle_ctau", &(bag.Particle_ctau), makeBranchName("Particle_ctau", "F").c_str());
    tree->Branch("Particle_barcode", &(bag.Particle_barcode), makeBranchName("Particle_barcode", "I").c_str());
    tree->Branch("Particle_pid", &(bag.Particle_pid), makeBranchName("Particle_pid", "I").c_str());
    
    tree->Branch("Particle_px", &(bag.Particle_px), makeBranchName("Particle_px", "F").c_str());
    tree->Branch("Particle_py", &(bag.Particle_py), makeBranchName("Particle_py", "F").c_str());
    tree->Branch("Particle_pz", &(bag.Particle_pz), makeBranchName("Particle_pz", "F").c_str());
    tree->Branch("Particle_energy", &(bag.Particle_energy), makeBranchName("Particle_energy", "F").c_str());
    tree->Branch("Particle_mass", &(bag.Particle_mass), makeBranchName("Particle_mass", "F").c_str());
    tree->Branch("Particle_status", &(bag.Particle_status), makeBranchName("Particle_status", "I").c_str());
    
    for(int i_daughter=0; i_daughter<n_daughters; i_daughter++){
      string branch_name = "Particle_d"+to_string(i_daughter);
      tree->Branch(branch_name.c_str(), &(bag.Particle_d[i_daughter]), makeBranchName(branch_name, "I").c_str());
    }
  }
  ~hepmc2root(){
    
  }
  
  TFile *file;
  TTree *tree;
  Bag bag;
  vector<TBranch*> branches;
  int pvertex[5000] = {0};
  ifstream inp;
  map<int, vector<int>> vertex;
  
  bool call(){
    
    vector<string> event;
    vector<string> token;
    string line;
    bool found_event = false;
    
    while(std::getline(inp, line)){
      
      event.push_back(line);
      token.clear();
    
      istringstream iss(line);
      string tmp;
      while(iss>>tmp) token.push_back(tmp);
    
      string key = token[0];
      if(key != "E") continue;
      
      found_event = true;
      break;
    }
    
    if(!found_event){
      cout<<"event not found, so returning"<<endl;
      return false;
    }
    
    if(token.size()==0){
      cout<<"** hepmc2root.py: can't find start of event"<<endl;
      exit(0);
    }
    
    bag.Event_number     = stoi(token[1]);
    bag.Event_numberMP   = stoi(token[2]);
    bag.Event_scale      = stod(token[3]);
    bag.Event_alphaQCD   = stod(token[4]);
    bag.Event_alphaQED   = stod(token[5]);
    bag.Event_processID  = stoi(token[6]);
    bag.Event_barcodeSPV = stoi(token[7]);
    bag.Event_numberV    = stoi(token[8]);
    bag.Event_barcodeBP1 = stoi(token[9]);
    bag.Event_barcodeBP2 = stoi(token[10]);
    bag.Event_numberP    = 0;
    
    vertex.clear();
    
    bool for_line_broken = false;
    
    while(std::getline(inp, line)){
      
      token.clear();
      event.push_back(line);
      
      istringstream iss(line);
      string tmp;
      while(iss>>tmp) token.push_back(tmp);
      
      string key = token[0];
      
      if(key == 'C'){
        bag.Xsection_value = stod(token[1]);
        bag.Xsection_error = stod(token[2]);
      }
      else if(key == 'F'){
        bag.PDF_parton1  = stoi(token[1]);
        bag.PDF_parton2  = stoi(token[2]);
        bag.PDF_x1       = stod(token[3]);
        bag.PDF_x2       = stod(token[4]);
        bag.PDF_Q2       = stod(token[5]);
        bag.PDF_x1f      = stod(token[6]);
        bag.PDF_x2f      = stod(token[7]);
        bag.PDF_id1      = stoi(token[8]);
        bag.PDF_id2      = stoi(token[9]);
        
      }
      else if(key == 'V'){
        int vbarcode = stoi(token[1]);
        
        vertex[vbarcode] = vector<int>(n_daughters, -1);
        
        float x    = stod(token[3]);
        float y    = stod(token[4]);
        float z    = stod(token[5]);
        float ctau = stod(token[6]);
        int nout = stoi(token[8]);
        
        for(int ii=0; ii<nout; ii++){
          bool for_broken = false;
          
          while(std::getline(inp, line)){
            
            token.clear();
            event.push_back(line);
            
            istringstream iss(line);
            string tmp;
            while(iss>>tmp) token.push_back(tmp);
            
            if(debug > 1){
              for(auto t : token) cout<<"\t "<< t;
              cout<<endl;
            }
            string key = token[0];
        
            if(key != 'P'){
              cout<<"** hepmc2root: faulty event record\n" << line << endl;
              exit(0);
            }
            
            if(bag.Event_numberP < MAXPART){

              int index = bag.Event_numberP;
              bag.Event_numberP++;
              
              bag.Particle_x[index]       = x;
              bag.Particle_y[index]       = y;
              bag.Particle_z[index]       = z;
              bag.Particle_ctau[index]    = ctau;
              
              bag.Particle_barcode[index] = stoi(token[1]);
              bag.Particle_pid[index]     = stoi(token[2]);
              bag.Particle_px[index]      = stod(token[3]);
              bag.Particle_py[index]      = stod(token[4]);
              bag.Particle_pz[index]      = stod(token[5]);
              bag.Particle_energy[index]  = stod(token[6]);
              bag.Particle_mass[index]    = stod(token[7]);
              bag.Particle_status[index]  = stoi(token[8]);
              pvertex[index] = stoi(token[11]);
              
              if(ii < vertex[vbarcode].size()){
                vertex[vbarcode][ii] = index;
              }
            }
            for_broken = true;
            break;
          }
          if(!for_broken) return false;
        }
      }
      
      if(vertex.size() >= bag.Event_numberV){
        for(int index=0; index<bag.Event_numberP; index++){
          int code = pvertex[index];
          
          if(vertex.find(code) != vertex.end()){
            for(int i=0; i<n_daughters; i++){
              bag.Particle_d[i][index] = vertex[code][i];
            }
          }
          else{
            for(int i=0; i<n_daughters; i++){
              bag.Particle_d[i][index] = -1;
            }
          }
        }
        file->cd();
        tree->Fill();
        return true;
      }
    }
    if(for_line_broken) return false;
    
    return true;
  }
};

int main(int argc, char *argv[])
{
  if(argc <= 1){
    cout<<"Usage: ./hepmc2root.py <HepMC-file> [output root file = <name>.root]"<<endl;
    exit(0);
  }
  
  string filename = argv[1];
  string outfilename = "";
  
  if(argc > 1) outfilename = argv[2];
  else{
    outfilename = filename.substr(filename.find_last_of("/\\") + 1);
    outfilename = std::regex_replace(outfilename, std::regex(".hepmc"), ".root");
  }
  
  auto stream = new hepmc2root(filename, outfilename);
  
  int ii = 0;
  while(stream->call()){
    if(ii % 100 == 0) cout<<ii<<endl;
    ii++;
  }

  stream->tree->Write("", TObject::kOverwrite);
  stream->file->Close();
  
}

