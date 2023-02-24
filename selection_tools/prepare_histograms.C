#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>

#include "Particle.hpp"
#include "Event.hpp"
#include "EventReader.hpp"

using namespace std;

int max_events = -1;
int n_daughters = 100;

TFile *input_file;

TTree* get_input_tree(string input_path)
{
  input_file = TFile::Open(input_path.c_str());
  
  if(!input_file){
    cout<<"ERROR -- could not open input file: "<<input_path<<endl;
    exit(0);
  }
  
  return (TTree*)input_file->Get("Events");
}

int main(int argc, char *argv[])
{
  if(argc != 3){
    cout<<"Usage: ./apply_selections input_path output_path"<<endl;
    exit(0);
  }
  
  string input_path = argv[1];
  string output_path = argv[2];
  
  auto input_tree = get_input_tree(input_path);
  auto output_file = new TFile(output_path.c_str(), "recreate");
  
// load events
  auto event_reader = EventReader(max_events, n_daughters);
  auto events = event_reader.read_events(input_tree);

  float logBins[1000];
  for (int i=0; i<1000;i++)
  {
    logBins[i] = (pow(10,log10(0)+((log10(100)-log10(0))/1000)*i));
  }
  
  map<string, TH1D*> hists = {
    {"muon_pt",  new TH1D("muon_pt", "muon_pt", 1000, 0, 1000)},
    {"muon_pz",  new TH1D("muon_pz", "muon_pz", 1000, -1000, 1000)},
    {"muon_mass",  new TH1D("muon_mass", "muon_mass", 1000, 0, 100)},
    {"muon_mass_logx",  new TH1D("muon_mass_logx", "muon_mass_logx", 1000, logBins)},
    {"muon_eta",  new TH1D("muon_eta", "muon_eta", 1000, -100, 100)},
    {"muon_phi",  new TH1D("muon_phi", "muon_phi", 1000, -100, 100)},
    {"muon_y",  new TH1D("muon_y", "muon_y", 1000, -100, 100)},
    {"muon_theta",  new TH1D("muon_theta", "muon_theta", 1000, -100, 100)},
    {"muon_lxy",  new TH1D("muon_lxy", "muon_lxy", 1000, 0, 100)},
    {"muon_lz",  new TH1D("muon_lz", "muon_lz", 1000, 0, 100)},
    {"muon_lxyz",  new TH1D("muon_lxyz", "muon_lxyz", 1000, 0, 100)},
    {"muon_ctau",  new TH1D("muon_ctau", "muon_ctau", 1000, 0, 100)},
    {"muon_boost",  new TH1D("muon_boost", "muon_boost", 1000, 0, 1000)},

    {"ss_muon_pt",  new TH1D("ss_muon_pt", "ss_muon_pt", 1000, 0, 1000)},
    {"ss_muon_pz",  new TH1D("ss_muon_pz", "ss_muon_pz", 1000, -1000, 1000)},
    {"ss_muon_mass",  new TH1D("ss_muon_mass", "ss_muon_mass", 1000, 0, 100)},
    {"ss_muon_eta",  new TH1D("ss_muon_eta", "ss_muon_eta", 1000, -100, 100)},
    {"ss_muon_phi",  new TH1D("ss_muon_phi", "ss_muon_phi", 1000, -100, 100)},
    {"ss_muon_y",  new TH1D("ss_muon_y", "ss_muon_y", 1000, -100, 100)},
    {"ss_muon_theta",  new TH1D("ss_muon_theta", "ss_muon_theta", 1000, -100, 100)},
    {"ss_muon_lxy",  new TH1D("ss_muon_lxy", "ss_muon_lxy", 1000, 0, 100)},
    {"ss_muon_lz",  new TH1D("ss_muon_lz", "ss_muon_lz", 1000, 0, 100)},
    {"ss_muon_lxyz",  new TH1D("ss_muon_lxyz", "ss_muon_lxyz", 1000, 0, 100)},
    {"ss_muon_ctau",  new TH1D("ss_muon_ctau", "ss_muon_ctau", 1000, 0, 100)},
    {"ss_muon_boost",  new TH1D("ss_muon_boost", "ss_muon_boost", 1000, 0, 1000)},

    {"dimuon_deltaR",  new TH1D("dimuon_deltaR", "dimuon_deltaR", 1000, 0, 100)},
    {"dimuon_deltaPhi",  new TH1D("dimuon_deltaPhi", "dimuon_deltaPhi", 1000, -100, 100)},

    {"ss_dimuon_deltaR",  new TH1D("ss_dimuon_deltaR", "ss_dimuon_deltaR", 1000, 0, 100)},
    {"ss_dimuon_deltaPhi",  new TH1D("ss_dimuon_deltaPhi", "ss_dimuon_deltaPhi", 1000, -100, 100)},

    {"dimuon_pt",  new TH1D("dimuon_pt", "dimuon_pt", 1000, 0, 1000)},
    {"dimuon_pz",  new TH1D("dimuon_pz", "dimuon_pz", 1000, -1000, 1000)},
    {"dimuon_mass",  new TH1D("dimuon_mass", "dimuon_mass", 1000, 0, 100)},
    {"dimuon_eta",  new TH1D("dimuon_eta", "dimuon_eta", 1000, -100, 100)},
    {"dimuon_phi",  new TH1D("dimuon_phi", "dimuon_phi", 1000, -100, 100)},

    {"ss_dimuon_pt",  new TH1D("ss_dimuon_pt", "ss_dimuon_pt", 1000, 0, 1000)},
    {"ss_dimuon_pz",  new TH1D("ss_dimuon_pz", "ss_dimuon_pz", 1000, -1000, 1000)},
    {"ss_dimuon_mass",  new TH1D("ss_dimuon_mass", "ss_dimuon_mass", 1000, 0, 100)},
    {"ss_dimuon_eta",  new TH1D("ss_dimuon_eta", "ss_dimuon_eta", 1000, -100, 100)},
    {"ss_dimuon_phi",  new TH1D("ss_dimuon_phi", "ss_dimuon_phi", 1000, -100, 100)},

    {"first_mother_pt",  new TH1D("first_mother_pt", "first_mother_pt", 1000, 0, 1000)},
    {"first_mother_pz",  new TH1D("first_mother_pz", "first_mother_pz", 1000, -1000, 1000)},
    {"first_mother_mass",  new TH1D("first_mother_mass", "first_mother_mass", 1000, 0, 200)},
    {"first_mother_eta",  new TH1D("first_mother_eta", "first_mother_eta", 1000, -100, 100)},
    {"first_mother_phi",  new TH1D("first_mother_phi", "first_mother_phi", 1000, -100, 100)},
    {"first_mother_lxy",  new TH1D("first_mother_lxy", "first_mother_lxy", 1000, 0, 100)},
    {"first_mother_lz",  new TH1D("first_mother_lz", "first_mother_lz", 1000, 0, 100)},
    {"first_mother_lxyz",  new TH1D("first_mother_lxyz", "first_mother_lxyz", 1000, 0, 100)},
    {"first_mother_ctau",  new TH1D("first_mother_ctau", "first_mother_ctau", 1000, 0, 100)},
    {"first_mother_boost",  new TH1D("first_mother_boost", "first_mother_boost", 1000, 0, 100)},

    {"ss_first_mother_pt",  new TH1D("ss_first_mother_pt", "ss_first_mother_pt", 1000, 0, 1000)},
    {"ss_first_mother_pz",  new TH1D("ss_first_mother_pz", "ss_first_mother_pz", 1000, -1000, 1000)},
    {"ss_first_mother_mass",  new TH1D("ss_first_mother_mass", "ss_first_mother_mass", 1000, 0, 200)},
    {"ss_first_mother_eta",  new TH1D("ss_first_mother_eta", "ss_first_mother_eta", 1000, -100, 100)},
    {"ss_first_mother_phi",  new TH1D("ss_first_mother_phi", "ss_first_mother_phi", 1000, -100, 100)},
    {"ss_first_mother_lxy",  new TH1D("ss_first_mother_lxy", "ss_first_mother_lxy", 1000, 0, 100)},
    {"ss_first_mother_lz",  new TH1D("ss_first_mother_lz", "ss_first_mother_lz", 1000, 0, 100)},
    {"ss_first_mother_lxyz",  new TH1D("ss_first_mother_lxyz", "ss_first_mother_lxyz", 1000, 0, 100)},
    {"ss_first_mother_ctau",  new TH1D("ss_first_mother_ctau", "ss_first_mother_ctau", 1000, 0, 100)},
    {"ss_first_mother_boost",  new TH1D("ss_first_mother_boost", "ss_first_mother_boost", 1000, 0, 100)},

    // Selection histograms
    {"sel_pT10_muon_pt",  new TH1D("sel_pT10_muon_pt", "sel_pT10_muon_pt", 1000, 0, 1000)},
    {"sel_pT10_muon_pz",  new TH1D("sel_pT10_muon_pz", "sel_pT10_muon_pz", 1000, -1000, 1000)},
    {"sel_pT10_muon_mass",  new TH1D("sel_pT10_muon_mass", "sel_pT10_muon_mass", 1000, 0, 100)},
    {"sel_pT10_muon_eta",  new TH1D("sel_pT10_muon_eta", "sel_pT10_muon_eta", 1000, -100, 100)},
    {"sel_pT10_muon_phi",  new TH1D("sel_pT10_muon_phi", "sel_pT10_muon_phi", 1000, -100, 100)},
    {"sel_pT10_muon_y",  new TH1D("sel_pT10_muon_y", "sel_pT10_muon_y", 1000, -100, 100)},
    {"sel_pT10_muon_theta",  new TH1D("sel_pT10_muon_theta", "sel_pT10_muon_theta", 1000, -100, 100)},
    {"sel_pT10_muon_lxy",  new TH1D("sel_pT10_muon_lxy", "sel_pT10_muon_lxy", 1000, 0, 100)},
    {"sel_pT10_muon_lz",  new TH1D("sel_pT10_muon_lz", "sel_pT10_muon_lz", 1000, 0, 100)},
    {"sel_pT10_muon_lxyz",  new TH1D("sel_pT10_muon_lxyz", "sel_pT10_muon_lxyz", 1000, 0, 100)},
    {"sel_pT10_muon_ctau",  new TH1D("sel_pT10_muon_ctau", "sel_pT10_muon_ctau", 1000, 0, 100)},
    {"sel_pT10_muon_boost",  new TH1D("sel_pT10_muon_boost", "sel_pT10_muon_boost", 1000, 0, 1000)},

    {"sel_pT10_dimuon_deltaR",  new TH1D("sel_pT10_dimuon_deltaR", "sel_pT10_dimuon_deltaR", 1000, 0, 100)},
    {"sel_pT10_dimuon_deltaPhi",  new TH1D("sel_pT10_dimuon_deltaPhi", "sel_pT10_dimuon_deltaPhi", 1000, -100, 100)},

    {"sel_pT10_dimuon_pt",  new TH1D("sel_pT10_dimuon_pt", "sel_pT10_dimuon_pt", 1000, 0, 1000)},
    {"sel_pT10_dimuon_pz",  new TH1D("sel_pT10_dimuon_pz", "sel_pT10_dimuon_pz", 1000, -1000, 1000)},
    {"sel_pT10_dimuon_mass",  new TH1D("sel_pT10_dimuon_mass", "sel_pT10_dimuon_mass", 1000, 0, 100)},
    {"sel_pT10_dimuon_eta",  new TH1D("sel_pT10_dimuon_eta", "sel_pT10_dimuon_eta", 1000, -100, 100)},
    {"sel_pT10_dimuon_phi",  new TH1D("sel_pT10_dimuon_phi", "sel_pT10_dimuon_phi", 1000, -100, 100)},

    {"sel_pT10_first_mother_pt",  new TH1D("sel_pT10_first_mother_pt", "sel_pT10_first_mother_pt", 1000, 0, 1000)},
    {"sel_pT10_first_mother_pz",  new TH1D("sel_pT10_first_mother_pz", "sel_pT10_first_mother_pz", 1000, -1000, 1000)},
    {"sel_pT10_first_mother_mass",  new TH1D("sel_pT10_first_mother_mass", "sel_pT10_first_mother_mass", 1000, 0, 200)},
    {"sel_pT10_first_mother_eta",  new TH1D("sel_pT10_first_mother_eta", "sel_pT10_first_mother_eta", 1000, -100, 100)},
    {"sel_pT10_first_mother_phi",  new TH1D("sel_pT10_first_mother_phi", "sel_pT10_first_mother_phi", 1000, -100, 100)},
    {"sel_pT10_first_mother_lxy",  new TH1D("sel_pT10_first_mother_lxy", "sel_pT10_first_mother_lxy", 1000, 0, 100)},
    {"sel_pT10_first_mother_lz",  new TH1D("sel_pT10_first_mother_lz", "sel_pT10_first_mother_lz", 1000, 0, 100)},
    {"sel_pT10_first_mother_lxyz",  new TH1D("sel_pT10_first_mother_lxyz", "sel_pT10_first_mother_lxyz", 1000, 0, 100)},
    {"sel_pT10_first_mother_ctau",  new TH1D("sel_pT10_first_mother_ctau", "sel_pT10_first_mother_ctau", 1000, 0, 100)},
    {"sel_pT10_first_mother_boost",  new TH1D("sel_pT10_first_mother_boost", "sel_pT10_first_mother_boost", 1000, 0, 100)},

    {"sel_pT10_ss_muon_pt",  new TH1D("sel_pT10_ss_muon_pt", "sel_pT10_ss_muon_pt", 1000, 0, 1000)},
    {"sel_pT10_ss_muon_pz",  new TH1D("sel_pT10_ss_muon_pz", "sel_pT10_ss_muon_pz", 1000, -1000, 1000)},
    {"sel_pT10_ss_muon_mass",  new TH1D("sel_pT10_ss_muon_mass", "sel_pT10_ss_muon_mass", 1000, 0, 100)},
    {"sel_pT10_ss_muon_eta",  new TH1D("sel_pT10_ss_muon_eta", "sel_pT10_ss_muon_eta", 1000, -100, 100)},
    {"sel_pT10_ss_muon_phi",  new TH1D("sel_pT10_ss_muon_phi", "sel_pT10_ss_muon_phi", 1000, -100, 100)},
    {"sel_pT10_ss_muon_y",  new TH1D("sel_pT10_ss_muon_y", "sel_pT10_ss_muon_y", 1000, -100, 100)},
    {"sel_pT10_ss_muon_theta",  new TH1D("sel_pT10_ss_muon_theta", "sel_pT10_ss_muon_theta", 1000, -100, 100)},
    {"sel_pT10_ss_muon_lxy",  new TH1D("sel_pT10_ss_muon_lxy", "sel_pT10_ss_muon_lxy", 1000, 0, 100)},
    {"sel_pT10_ss_muon_lz",  new TH1D("sel_pT10_ss_muon_lz", "sel_pT10_ss_muon_lz", 1000, 0, 100)},
    {"sel_pT10_ss_muon_lxyz",  new TH1D("sel_pT10_ss_muon_lxyz", "sel_pT10_ss_muon_lxyz", 1000, 0, 100)},
    {"sel_pT10_ss_muon_ctau",  new TH1D("sel_pT10_ss_muon_ctau", "sel_pT10_ss_muon_ctau", 1000, 0, 100)},
    {"sel_pT10_ss_muon_boost",  new TH1D("sel_pT10_ss_muon_boost", "sel_pT10_ss_muon_boost", 1000, 0, 1000)},

    {"sel_pT10_ss_dimuon_deltaR",  new TH1D("sel_pT10_ss_dimuon_deltaR", "sel_pT10_ss_dimuon_deltaR", 1000, 0, 100)},
    {"sel_pT10_ss_dimuon_deltaPhi",  new TH1D("sel_pT10_ss_dimuon_deltaPhi", "sel_pT10_ss_dimuon_deltaPhi", 1000, -100, 100)},

    {"sel_pT10_ss_dimuon_pt",  new TH1D("sel_pT10_ss_dimuon_pt", "sel_pT10_ss_dimuon_pt", 1000, 0, 1000)},
    {"sel_pT10_ss_dimuon_pz",  new TH1D("sel_pT10_ss_dimuon_pz", "sel_pT10_ss_dimuon_pz", 1000, -1000, 1000)},
    {"sel_pT10_ss_dimuon_mass",  new TH1D("sel_pT10_ss_dimuon_mass", "sel_pT10_ss_dimuon_mass", 1000, 0, 100)},
    {"sel_pT10_ss_dimuon_eta",  new TH1D("sel_pT10_ss_dimuon_eta", "sel_pT10_ss_dimuon_eta", 1000, -100, 100)},
    {"sel_pT10_ss_dimuon_phi",  new TH1D("sel_pT10_ss_dimuon_phi", "sel_pT10_ss_dimuon_phi", 1000, -100, 100)},

    {"sel_pT10_ss_first_mother_pt",  new TH1D("sel_pT10_ss_first_mother_pt", "sel_pT10_ss_first_mother_pt", 1000, 0, 1000)},
    {"sel_pT10_ss_first_mother_pz",  new TH1D("sel_pT10_ss_first_mother_pz", "sel_pT10_ss_first_mother_pz", 1000, -1000, 1000)},
    {"sel_pT10_ss_first_mother_mass",  new TH1D("sel_pT10_ss_first_mother_mass", "sel_pT10_ss_first_mother_mass", 1000, 0, 200)},
    {"sel_pT10_ss_first_mother_eta",  new TH1D("sel_pT10_ss_first_mother_eta", "sel_pT10_ss_first_mother_eta", 1000, -100, 100)},
    {"sel_pT10_ss_first_mother_phi",  new TH1D("sel_pT10_ss_first_mother_phi", "sel_pT10_ss_first_mother_phi", 1000, -100, 100)},
    {"sel_pT10_ss_first_mother_lxy",  new TH1D("sel_pT10_ss_first_mother_lxy", "sel_pT10_ss_first_mother_lxy", 1000, 0, 100)},
    {"sel_pT10_ss_first_mother_lz",  new TH1D("sel_pT10_ss_first_mother_lz", "sel_pT10_ss_first_mother_lz", 1000, 0, 100)},
    {"sel_pT10_ss_first_mother_lxyz",  new TH1D("sel_pT10_ss_first_mother_lxyz", "sel_pT10_ss_first_mother_lxyz", 1000, 0, 100)},
    {"sel_pT10_ss_first_mother_ctau",  new TH1D("sel_pT10_ss_first_mother_ctau", "sel_pT10_ss_first_mother_ctau", 1000, 0, 100)},
    {"sel_pT10_ss_first_mother_boost",  new TH1D("sel_pT10_ss_first_mother_boost", "sel_pT10_ss_first_mother_boost", 1000, 0, 100)},

    {"sel_pT10_Jpsimass_muon_pt",  new TH1D("sel_pT10_Jpsimass_muon_pt", "sel_pT10_Jpsimass_muon_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_muon_pz",  new TH1D("sel_pT10_Jpsimass_muon_pz", "sel_pT10_Jpsimass_muon_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_muon_mass",  new TH1D("sel_pT10_Jpsimass_muon_mass", "sel_pT10_Jpsimass_muon_mass", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_muon_eta",  new TH1D("sel_pT10_Jpsimass_muon_eta", "sel_pT10_Jpsimass_muon_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_muon_phi",  new TH1D("sel_pT10_Jpsimass_muon_phi", "sel_pT10_Jpsimass_muon_phi", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_muon_y",  new TH1D("sel_pT10_Jpsimass_muon_y", "sel_pT10_Jpsimass_muon_y", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_muon_theta",  new TH1D("sel_pT10_Jpsimass_muon_theta", "sel_pT10_Jpsimass_muon_theta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_muon_lxy",  new TH1D("sel_pT10_Jpsimass_muon_lxy", "sel_pT10_Jpsimass_muon_lxy", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_muon_lz",  new TH1D("sel_pT10_Jpsimass_muon_lz", "sel_pT10_Jpsimass_muon_lz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_muon_lxyz",  new TH1D("sel_pT10_Jpsimass_muon_lxyz", "sel_pT10_Jpsimass_muon_lxyz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_muon_ctau",  new TH1D("sel_pT10_Jpsimass_muon_ctau", "sel_pT10_Jpsimass_muon_ctau", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_muon_boost",  new TH1D("sel_pT10_Jpsimass_muon_boost", "sel_pT10_Jpsimass_muon_boost", 1000, 0, 1000)},

    {"sel_pT10_Jpsimass_dimuon_deltaR",  new TH1D("sel_pT10_Jpsimass_dimuon_deltaR", "sel_pT10_Jpsimass_dimuon_deltaR", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_dimuon_deltaPhi",  new TH1D("sel_pT10_Jpsimass_dimuon_deltaPhi", "sel_pT10_Jpsimass_dimuon_deltaPhi", 1000, -100, 100)},

    {"sel_pT10_Jpsimass_dimuon_pt",  new TH1D("sel_pT10_Jpsimass_dimuon_pt", "sel_pT10_Jpsimass_dimuon_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_dimuon_pz",  new TH1D("sel_pT10_Jpsimass_dimuon_pz", "sel_pT10_Jpsimass_dimuon_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_dimuon_mass",  new TH1D("sel_pT10_Jpsimass_dimuon_mass", "sel_pT10_Jpsimass_dimuon_mass", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_dimuon_eta",  new TH1D("sel_pT10_Jpsimass_dimuon_eta", "sel_pT10_Jpsimass_dimuon_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_dimuon_phi",  new TH1D("sel_pT10_Jpsimass_dimuon_phi", "sel_pT10_Jpsimass_dimuon_phi", 1000, -100, 100)},

    {"sel_pT10_Jpsimass_first_mother_pt",  new TH1D("sel_pT10_Jpsimass_first_mother_pt", "sel_pT10_Jpsimass_first_mother_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_first_mother_pz",  new TH1D("sel_pT10_Jpsimass_first_mother_pz", "sel_pT10_Jpsimass_first_mother_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_first_mother_mass",  new TH1D("sel_pT10_Jpsimass_first_mother_mass", "sel_pT10_Jpsimass_first_mother_mass", 1000, 0, 200)},
    {"sel_pT10_Jpsimass_first_mother_eta",  new TH1D("sel_pT10_Jpsimass_first_mother_eta", "sel_pT10_Jpsimass_first_mother_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_first_mother_phi",  new TH1D("sel_pT10_Jpsimass_first_mother_phi", "sel_pT10_Jpsimass_first_mother_phi", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_first_mother_lxy",  new TH1D("sel_pT10_Jpsimass_first_mother_lxy", "sel_pT10_Jpsimass_first_mother_lxy", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_first_mother_lz",  new TH1D("sel_pT10_Jpsimass_first_mother_lz", "sel_pT10_Jpsimass_first_mother_lz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_first_mother_lxyz",  new TH1D("sel_pT10_Jpsimass_first_mother_lxyz", "sel_pT10_Jpsimass_first_mother_lxyz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_first_mother_ctau",  new TH1D("sel_pT10_Jpsimass_first_mother_ctau", "sel_pT10_Jpsimass_first_mother_ctau", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_first_mother_boost",  new TH1D("sel_pT10_Jpsimass_first_mother_boost", "sel_pT10_Jpsimass_first_mother_boost", 1000, 0, 100)},

    {"sel_pT10_Jpsimass_ss_muon_pt",  new TH1D("sel_pT10_Jpsimass_ss_muon_pt", "sel_pT10_Jpsimass_ss_muon_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_ss_muon_pz",  new TH1D("sel_pT10_Jpsimass_ss_muon_pz", "sel_pT10_Jpsimass_ss_muon_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_ss_muon_mass",  new TH1D("sel_pT10_Jpsimass_ss_muon_mass", "sel_pT10_Jpsimass_ss_muon_mass", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_muon_eta",  new TH1D("sel_pT10_Jpsimass_ss_muon_eta", "sel_pT10_Jpsimass_ss_muon_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_muon_phi",  new TH1D("sel_pT10_Jpsimass_ss_muon_phi", "sel_pT10_Jpsimass_ss_muon_phi", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_muon_y",  new TH1D("sel_pT10_Jpsimass_ss_muon_y", "sel_pT10_Jpsimass_ss_muon_y", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_muon_theta",  new TH1D("sel_pT10_Jpsimass_ss_muon_theta", "sel_pT10_Jpsimass_ss_muon_theta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_muon_lxy",  new TH1D("sel_pT10_Jpsimass_ss_muon_lxy", "sel_pT10_Jpsimass_ss_muon_lxy", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_muon_lz",  new TH1D("sel_pT10_Jpsimass_ss_muon_lz", "sel_pT10_Jpsimass_ss_muon_lz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_muon_lxyz",  new TH1D("sel_pT10_Jpsimass_ss_muon_lxyz", "sel_pT10_Jpsimass_ss_muon_lxyz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_muon_ctau",  new TH1D("sel_pT10_Jpsimass_ss_muon_ctau", "sel_pT10_Jpsimass_ss_muon_ctau", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_muon_boost",  new TH1D("sel_pT10_Jpsimass_ss_muon_boost", "sel_pT10_Jpsimass_ss_muon_boost", 1000, 0, 1000)},

    {"sel_pT10_Jpsimass_ss_dimuon_deltaR",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_deltaR", "sel_pT10_Jpsimass_ss_dimuon_deltaR", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_dimuon_deltaPhi",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_deltaPhi", "sel_pT10_Jpsimass_ss_dimuon_deltaPhi", 1000, -100, 100)},

    {"sel_pT10_Jpsimass_ss_dimuon_pt",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_pt", "sel_pT10_Jpsimass_ss_dimuon_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_ss_dimuon_pz",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_pz", "sel_pT10_Jpsimass_ss_dimuon_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_ss_dimuon_mass",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_mass", "sel_pT10_Jpsimass_ss_dimuon_mass", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_dimuon_eta",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_eta", "sel_pT10_Jpsimass_ss_dimuon_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_dimuon_phi",  new TH1D("sel_pT10_Jpsimass_ss_dimuon_phi", "sel_pT10_Jpsimass_ss_dimuon_phi", 1000, -100, 100)},

    {"sel_pT10_Jpsimass_ss_first_mother_pt",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_pt", "sel_pT10_Jpsimass_ss_first_mother_pt", 1000, 0, 1000)},
    {"sel_pT10_Jpsimass_ss_first_mother_pz",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_pz", "sel_pT10_Jpsimass_ss_first_mother_pz", 1000, -1000, 1000)},
    {"sel_pT10_Jpsimass_ss_first_mother_mass",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_mass", "sel_pT10_Jpsimass_ss_first_mother_mass", 1000, 0, 200)},
    {"sel_pT10_Jpsimass_ss_first_mother_eta",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_eta", "sel_pT10_Jpsimass_ss_first_mother_eta", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_phi",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_phi", "sel_pT10_Jpsimass_ss_first_mother_phi", 1000, -100, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_lxy",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_lxy", "sel_pT10_Jpsimass_ss_first_mother_lxy", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_lz",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_lz", "sel_pT10_Jpsimass_ss_first_mother_lz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_lxyz",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_lxyz", "sel_pT10_Jpsimass_ss_first_mother_lxyz", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_ctau",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_ctau", "sel_pT10_Jpsimass_ss_first_mother_ctau", 1000, 0, 100)},
    {"sel_pT10_Jpsimass_ss_first_mother_boost",  new TH1D("sel_pT10_Jpsimass_ss_first_mother_boost", "sel_pT10_Jpsimass_ss_first_mother_boost", 1000, 0, 100)},
  };
  
  
  auto fill_single_muon_hists = [&](const Particle *muon)->void {
    hists["muon_pt"]->Fill(muon->four_vector.Pt());
    hists["muon_pz"]->Fill(muon->four_vector.Pz());
    hists["muon_mass_logx"]->Fill(muon->four_vector.M());
    hists["muon_mass"]->Fill(muon->four_vector.M());
    hists["muon_eta"]->Fill(muon->four_vector.Eta());
    hists["muon_phi"]->Fill(muon->four_vector.Phi());
    hists["muon_y"]->Fill(muon->four_vector.Rapidity());
    hists["muon_theta"]->Fill(muon->four_vector.Theta());
    hists["muon_lxy"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2)));
    hists["muon_lz"]->Fill(muon->z);
    hists["muon_lxyz"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2) + pow(muon->z, 2)));
    hists["muon_ctau"]->Fill(muon->ctau);
    hists["muon_boost"]->Fill(muon->momentum()/muon->mass);
  };

  auto fill_double_muon_hists =  [&](const Particle *muon1,const Particle *muon2)->void {
    hists["dimuon_deltaPhi"]->Fill(muon1->four_vector.DeltaPhi(muon2->four_vector));
    hists["dimuon_deltaR"]->Fill(muon1->four_vector.DeltaR(muon2->four_vector));
  };
  
  auto fill_dimuon_hists = [&](const TLorentzVector &dimuon)->void {
    hists["dimuon_pt"]->Fill(dimuon.Pt());
    hists["dimuon_pz"]->Fill(dimuon.Pz());
    hists["dimuon_mass"]->Fill(dimuon.M());
    hists["dimuon_eta"]->Fill(dimuon.Eta());
    hists["dimuon_phi"]->Fill(dimuon.Phi());
  };
  
  auto fill_first_mother_hists = [&](const Particle *mother)->void {
    hists["first_mother_pt"]->Fill(mother->four_vector.Pt());
    hists["first_mother_pz"]->Fill(mother->four_vector.Pz());
    hists["first_mother_mass"]->Fill(mother->four_vector.M());
    hists["first_mother_eta"]->Fill(mother->four_vector.Eta());
    hists["first_mother_phi"]->Fill(mother->four_vector.Phi());
    hists["first_mother_lxy"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2)));
    hists["first_mother_lz"]->Fill(mother->z);
    hists["first_mother_lxyz"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2) + pow(mother->z, 2)));
    hists["first_mother_ctau"]->Fill(mother->ctau);
    hists["first_mother_boost"]->Fill(mother->momentum()/mother->mass);
  };

  auto fill_ss_single_muon_hists = [&](const Particle *muon)->void {
    hists["ss_muon_pt"]->Fill(muon->four_vector.Pt());
    hists["ss_muon_pz"]->Fill(muon->four_vector.Pz());
    hists["ss_muon_mass"]->Fill(muon->four_vector.M());
    hists["ss_muon_eta"]->Fill(muon->four_vector.Eta());
    hists["ss_muon_phi"]->Fill(muon->four_vector.Phi());
    hists["ss_muon_y"]->Fill(muon->four_vector.Rapidity());
    hists["ss_muon_theta"]->Fill(muon->four_vector.Theta());
    hists["ss_muon_lxy"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2)));
    hists["ss_muon_lz"]->Fill(muon->z);
    hists["ss_muon_lxyz"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2) + pow(muon->z, 2)));
    hists["ss_muon_ctau"]->Fill(muon->ctau);
    hists["ss_muon_boost"]->Fill(muon->momentum()/muon->mass);
  };

  auto fill_ss_double_muon_hists =  [&](const Particle *muon1,const Particle *muon2)->void {
    hists["ss_dimuon_deltaPhi"]->Fill(muon1->four_vector.DeltaPhi(muon2->four_vector));
    hists["ss_dimuon_deltaR"]->Fill(muon1->four_vector.DeltaR(muon2->four_vector));
  };
  
  auto fill_ss_dimuon_hists = [&](const TLorentzVector &dimuon)->void {
    hists["ss_dimuon_pt"]->Fill(dimuon.Pt());
    hists["ss_dimuon_pz"]->Fill(dimuon.Pz());
    hists["ss_dimuon_mass"]->Fill(dimuon.M());
    hists["ss_dimuon_eta"]->Fill(dimuon.Eta());
    hists["ss_dimuon_phi"]->Fill(dimuon.Phi());
  };
  
  auto fill_ss_first_mother_hists = [&](const Particle *mother)->void {
    hists["ss_first_mother_pt"]->Fill(mother->four_vector.Pt());
    hists["ss_first_mother_pz"]->Fill(mother->four_vector.Pz());
    hists["ss_first_mother_mass"]->Fill(mother->four_vector.M());
    hists["ss_first_mother_eta"]->Fill(mother->four_vector.Eta());
    hists["ss_first_mother_phi"]->Fill(mother->four_vector.Phi());
    hists["ss_first_mother_lxy"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2)));
    hists["ss_first_mother_lz"]->Fill(mother->z);
    hists["ss_first_mother_lxyz"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2) + pow(mother->z, 2)));
    hists["ss_first_mother_ctau"]->Fill(mother->ctau);
    hists["ss_first_mother_boost"]->Fill(mother->momentum()/mother->mass);
  };

  auto fill_sel_single_muon_hists = [&](const Particle *muon, const string sel)->void {
    hists[sel + "muon_pt"]->Fill(muon->four_vector.Pt());
    hists[sel + "muon_pz"]->Fill(muon->four_vector.Pt());
    hists[sel + "muon_mass"]->Fill(muon->four_vector.M());
    hists[sel + "muon_eta"]->Fill(muon->four_vector.Eta());
    hists[sel + "muon_phi"]->Fill(muon->four_vector.Eta());
    hists[sel + "muon_y"]->Fill(muon->four_vector.Eta());
    hists[sel + "muon_theta"]->Fill(muon->four_vector.Eta());
    hists[sel + "muon_lxy"]->Fill(muon->four_vector.Phi());
    hists[sel + "muon_lz"]->Fill(muon->four_vector.Phi());
    hists[sel + "muon_lxyz"]->Fill(muon->four_vector.Phi());
    hists[sel + "muon_ctau"]->Fill(muon->four_vector.Rapidity());
    hists[sel + "muon_boost"]->Fill(muon->four_vector.Theta());
  };

  auto fill_sel_double_muon_hists =  [&](const Particle *muon1,const Particle *muon2, const string sel)->void {
    hists[sel + "dimuon_deltaPhi"]->Fill(muon1->four_vector.DeltaPhi(muon2->four_vector));
    hists[sel + "dimuon_deltaR"]->Fill(muon1->four_vector.DeltaR(muon2->four_vector));
  };
  
  auto fill_sel_dimuon_hists = [&](const TLorentzVector &dimuon, const string sel)->void {
    hists[sel + "dimuon_pt"]->Fill(dimuon.Pt());
    hists[sel + "dimuon_pz"]->Fill(dimuon.Pz());
    hists[sel + "dimuon_mass"]->Fill(dimuon.M());
    hists[sel + "dimuon_eta"]->Fill(dimuon.Eta());
    hists[sel + "dimuon_phi"]->Fill(dimuon.Phi());
  };
  
  auto fill_sel_first_mother_hists = [&](const Particle *mother, const string sel)->void {
    hists[sel + "first_mother_pt"]->Fill(mother->four_vector.Pt());
    hists[sel + "first_mother_pz"]->Fill(mother->four_vector.Pz());
    hists[sel + "first_mother_mass"]->Fill(mother->four_vector.M());
    hists[sel + "first_mother_eta"]->Fill(mother->four_vector.Eta());
    hists[sel + "first_mother_phi"]->Fill(mother->four_vector.Phi());
    hists[sel + "first_mother_lxy"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2)));
    hists[sel + "first_mother_lz"]->Fill(mother->z);
    hists[sel + "first_mother_lxyz"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2) + pow(mother->z, 2)));
    hists[sel + "first_mother_ctau"]->Fill(mother->ctau);
    hists[sel + "first_mother_boost"]->Fill(mother->momentum()/mother->mass);
  };

  auto fill_sel_ss_single_muon_hists = [&](const Particle *muon, const string sel)->void {
    hists[sel + "ss_muon_pt"]->Fill(muon->four_vector.Pt());
    hists[sel + "ss_muon_pz"]->Fill(muon->four_vector.Pt());
    hists[sel + "ss_muon_mass"]->Fill(muon->four_vector.M());
    hists[sel + "ss_muon_eta"]->Fill(muon->four_vector.Eta());
    hists[sel + "ss_muon_phi"]->Fill(muon->four_vector.Eta());
    hists[sel + "ss_muon_y"]->Fill(muon->four_vector.Eta());
    hists[sel + "ss_muon_theta"]->Fill(muon->four_vector.Eta());
    hists[sel + "ss_muon_lxy"]->Fill(muon->four_vector.Phi());
    hists[sel + "ss_muon_lz"]->Fill(muon->four_vector.Phi());
    hists[sel + "ss_muon_lxyz"]->Fill(muon->four_vector.Phi());
    hists[sel + "ss_muon_ctau"]->Fill(muon->four_vector.Rapidity());
    hists[sel + "ss_muon_boost"]->Fill(muon->four_vector.Theta());
  };

  auto fill_sel_ss_double_muon_hists =  [&](const Particle *muon1,const Particle *muon2, const string sel)->void {
    hists[sel + "ss_dimuon_deltaPhi"]->Fill(muon1->four_vector.DeltaPhi(muon2->four_vector));
    hists[sel + "ss_dimuon_deltaR"]->Fill(muon1->four_vector.DeltaR(muon2->four_vector));
  };
  
  auto fill_sel_ss_dimuon_hists = [&](const TLorentzVector &dimuon, const string sel)->void {
    hists[sel + "ss_dimuon_pt"]->Fill(dimuon.Pt());
    hists[sel + "ss_dimuon_pz"]->Fill(dimuon.Pz());
    hists[sel + "ss_dimuon_mass"]->Fill(dimuon.M());
    hists[sel + "ss_dimuon_eta"]->Fill(dimuon.Eta());
    hists[sel + "ss_dimuon_phi"]->Fill(dimuon.Phi());
  };
  
  auto fill_sel_ss_first_mother_hists = [&](const Particle *mother, const string sel)->void {
    hists[sel + "ss_first_mother_pt"]->Fill(mother->four_vector.Pt());
    hists[sel + "ss_first_mother_pz"]->Fill(mother->four_vector.Pz());
    hists[sel + "ss_first_mother_mass"]->Fill(mother->four_vector.M());
    hists[sel + "ss_first_mother_eta"]->Fill(mother->four_vector.Eta());
    hists[sel + "ss_first_mother_phi"]->Fill(mother->four_vector.Phi());
    hists[sel + "ss_first_mother_lxy"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2)));
    hists[sel + "ss_first_mother_lz"]->Fill(mother->z);
    hists[sel + "ss_first_mother_lxyz"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2) + pow(mother->z, 2)));
    hists[sel + "ss_first_mother_ctau"]->Fill(mother->ctau);
    hists[sel + "ss_first_mother_boost"]->Fill(mother->momentum()/mother->mass);
  };
  
  int i_event=0;
  
  for(auto event : events){
    
    i_event++;
    
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 1){ // single muon tree
      auto muon = event->get_single_muon();
      
      if(!muon){
        cout<<"\n\nERROR -- single muon not found in an event passing single muon preselection...\n\n"<<endl;
        continue;
      }
      
      fill_single_muon_hists(muon);
      
      // TODO: handle properly multiple mothers case
      auto mother = event->particles[muon->mothers[0]];
      fill_first_mother_hists(mother);

      if (muon->four_vector.Pt() > 10)
      {
        string sel = "sel_pT10_";
        fill_sel_single_muon_hists(muon,sel);
        fill_sel_first_mother_hists(mother,sel);
      }
    }
    else if(preselection_code == 2){ // pair category
      auto muons = event->get_muon_pair();
      
      for(auto muon_pair : muons){
        auto muon_1 = get<0>(muon_pair);
        auto muon_2 = get<1>(muon_pair);
        
        fill_single_muon_hists(muon_1);
        fill_single_muon_hists(muon_2);
        
        TLorentzVector dimuon = muon_1->four_vector + muon_2->four_vector;
        fill_dimuon_hists(dimuon);
        fill_double_muon_hists(muon_1, muon_2);
        
        // TODO: handle the full chain of mother (and multiple mothers) correctly
        auto mother = event->particles[muon_1->mothers[0]];
        fill_first_mother_hists(mother);

        if (muon_1->four_vector.Pt() > 10 && muon_2->four_vector.Pt() > 10)
        {
          string sel = "sel_pT10_";
          fill_sel_single_muon_hists(muon_1,sel);
          fill_sel_single_muon_hists(muon_2,sel);
          fill_sel_dimuon_hists(dimuon,sel);
          fill_sel_first_mother_hists(mother,sel);
          if (muon_1->four_vector.M() <= 2900 || muon_1->four_vector.M() <= 3300)
          {
            if (muon_2->four_vector.M() <= 2900 || muon_2->four_vector.M() <= 3300)
            {
              string sel = "sel_pT10_Jpsimass_";
              fill_sel_single_muon_hists(muon_1,sel);
              fill_sel_single_muon_hists(muon_2,sel);
              fill_sel_dimuon_hists(dimuon,sel);
              fill_sel_first_mother_hists(mother,sel);
            }
          }
        }
      }
    }
    else if(preselection_code == 3){ // non-pair category
      
      // Fill in hists for the opposite sign non-pair (if exists)
      auto [opposite_sign_muon_1, opposite_sign_muon_2] = event->get_smallest_deltaR_opposite_sign_muon_non_pair();
      
      if(opposite_sign_muon_1 && opposite_sign_muon_2){
        fill_single_muon_hists(opposite_sign_muon_1);
        fill_single_muon_hists(opposite_sign_muon_2);
        TLorentzVector dimuon = opposite_sign_muon_1->four_vector + opposite_sign_muon_2->four_vector;
        fill_dimuon_hists(dimuon);
        fill_double_muon_hists(opposite_sign_muon_1,opposite_sign_muon_2);
        
        auto mother_1 = event->particles[opposite_sign_muon_1->mothers[0]];
        fill_first_mother_hists(mother_1);
        
        auto mother_2 = event->particles[opposite_sign_muon_2->mothers[0]];
        fill_first_mother_hists(mother_2);

        if (opposite_sign_muon_1->four_vector.Pt() > 10 && opposite_sign_muon_2->four_vector.Pt() > 10)
        {
          string sel = "sel_pT10_";
          fill_sel_single_muon_hists(opposite_sign_muon_1,sel);
          fill_sel_single_muon_hists(opposite_sign_muon_2,sel);
          fill_sel_dimuon_hists(dimuon,sel);
          fill_sel_first_mother_hists(mother_1,sel);
          fill_sel_first_mother_hists(mother_2,sel);
          if (opposite_sign_muon_1->four_vector.M() <= 2900 || opposite_sign_muon_1->four_vector.M() <= 3300)
          {
            if (opposite_sign_muon_2->four_vector.M() <= 2900 || opposite_sign_muon_2->four_vector.M() <= 3300)
            {
              string sel = "sel_pT10_Jpsimass_";
              fill_sel_single_muon_hists(opposite_sign_muon_1,sel);
              fill_sel_single_muon_hists(opposite_sign_muon_2,sel);
              fill_sel_dimuon_hists(dimuon,sel);
              fill_sel_first_mother_hists(mother_1,sel);
              fill_sel_first_mother_hists(mother_2,sel);
            }
          }
        }
      }
      
      // Fill in hists for the opposite sign non-pair (if exists)
      auto [same_sign_muon_1, same_sign_muon_2] = event->get_smallest_deltaR_same_sign_muon_non_pair();
      
      if(same_sign_muon_1 && same_sign_muon_2){
        fill_ss_single_muon_hists(same_sign_muon_1);
        fill_ss_single_muon_hists(same_sign_muon_2);
        TLorentzVector dimuon = same_sign_muon_1->four_vector + same_sign_muon_2->four_vector;
        fill_ss_dimuon_hists(dimuon);
        fill_ss_double_muon_hists(same_sign_muon_1,same_sign_muon_1);
        
        auto mother_1 = event->particles[same_sign_muon_1->mothers[0]];
        fill_ss_first_mother_hists(mother_1);
        
        auto mother_2 = event->particles[same_sign_muon_2->mothers[0]];
        fill_ss_first_mother_hists(mother_2);

        if (same_sign_muon_1->four_vector.Pt() > 10 && same_sign_muon_2->four_vector.Pt() > 10)
        {
          string sel = "sel_pT10_";
          fill_sel_ss_single_muon_hists(same_sign_muon_1,sel);
          fill_sel_ss_single_muon_hists(same_sign_muon_1,sel);
          fill_sel_ss_dimuon_hists(dimuon,sel);
          fill_sel_ss_first_mother_hists(mother_1,sel);
          fill_sel_ss_first_mother_hists(mother_2,sel);
          if (same_sign_muon_1->four_vector.M() <= 2900 || same_sign_muon_1->four_vector.M() <= 3300)
          {
            if (same_sign_muon_2->four_vector.M() <= 2900 || same_sign_muon_2->four_vector.M() <= 3300)
            {
              string sel = "sel_pT10_Jpsimass_";
              fill_sel_ss_single_muon_hists(same_sign_muon_1,sel);
              fill_sel_ss_single_muon_hists(same_sign_muon_1,sel);
              fill_sel_ss_dimuon_hists(dimuon,sel);
              fill_sel_ss_first_mother_hists(mother_1,sel);
              fill_sel_ss_first_mother_hists(mother_2,sel);
            }
          }
        }
      }
      
    }
  }
  
  // close files
  output_file->cd();
  for(auto &[name, hist] : hists) hist->Write();
  
  input_file->Close();
  output_file->Close();
  
  return 0;
}
