/*
Simple macro showing how to access branches from the delphes output root file,
loop over events, and plot simple quantities such as the jet pt and the di-electron invariant
mass.

root -l examples/Example1.C'("combined_had_lep_samples/RH_500GeV.root")'

*/

#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#endif
#include "TLorentzVector.h"
#include "TFile.h"
#include "TTree.h"

//------------------------------------------------------------------------------



typedef struct {
  Float_t  lep_pt;
  Float_t  lep_eta;
  Float_t  lep_phi;

  Float_t  jet_pt;
  Float_t  jet_eta;
  Float_t  jet_phi;
  Float_t  jet_btag;

  Float_t  met_pt;
  Float_t  met_phi;
  Float_t  met_eta;

  Float_t  mt;
  Float_t  mlb;
  Float_t  ratio;
  Int_t  RightHanded;


} leptonic_variables;


typedef struct {
  Float_t  jj_pt;
  Float_t  jj_eta;
  Float_t  jj_phi;

  Float_t  bjet_pt;
  Float_t  bjet_eta;
  Float_t  bjet_phi;
 

  Float_t  met_pt;
  Float_t  met_phi;
  Float_t  met_eta;

  Float_t  mjjb;
  Float_t  ratio;
  Float_t  mjb;
  Float_t  ratiojb;
  Int_t  RightHanded;


} hadronic_variables;



Float_t* returnJetStuff(Float_t values[7], Jet *bjet, Jet *jet1, Jet *jet2){

  TLorentzVector TL_b;
  TL_b.SetPtEtaPhiM(bjet->PT, bjet->Eta, bjet->Phi, bjet->Mass );
  TLorentzVector TL_j1;
  TL_j1.SetPtEtaPhiM(jet1->PT, jet1->Eta, jet1->Phi, jet1->Mass );
  TLorentzVector TL_j2;
  TL_j2.SetPtEtaPhiM(jet2->PT, jet2->Eta, jet2->Phi, jet2->Mass );
  TLorentzVector TL_w;
  TL_w = TL_j2 + TL_j1;

  values[0] = (TL_w + TL_b).M();
  values[1] =  TL_b.E()/(TL_w + TL_b).E();
  values[2] =  TL_w.Pt();
  values[3] =  TL_w.Eta();
  values[4] =  TL_w.Phi();
  values[5] =  (TL_j1 + TL_b).M();
  values[6] =  TL_b.E()/(TL_j1 + TL_b).E();

  return values;
}


void make_short_tree(const char *inputFile, const char *outputFile, int rightHanded)
{
  gSystem->Load("libDelphes");

  // Create chain of root trees
  TChain chain("Delphes");
  chain.Add(inputFile);


  // make leptonTTree.C
  TFile f(outputFile,"recreate");
  TTree TTree_lep("TTree_lep","TTree_lep");
  leptonic_variables lep;
  
  
  TTree_lep.Branch("lep_pt", &lep.lep_pt, "lep_pt/F");
  TTree_lep.Branch("lep_eta", &lep.lep_eta, "lep_eta/F");
  TTree_lep.Branch("lep_phi", &lep.lep_phi, "lep_phi/F");
  
  TTree_lep.Branch("jet_pt", &lep.jet_pt, "jet_pt/F");
  TTree_lep.Branch("jet_eta", &lep.jet_eta, "jet_eta/F");
  TTree_lep.Branch("jet_phi", &lep.jet_phi, "jet_phi/F");
  TTree_lep.Branch("jet_btag", &lep.jet_btag, "jet_btag/F");
  
  TTree_lep.Branch("met_pt", &lep.met_pt, "met_pt/F");
  TTree_lep.Branch("met_phi", &lep.met_phi, "met_phi/F");
  TTree_lep.Branch("met_eta", &lep.met_eta, "met_eta/F");
  
  TTree_lep.Branch("ratio", &lep.ratio, "ratio/F");
  TTree_lep.Branch("mt", &lep.mt, "mt/F");
  TTree_lep.Branch("mlb", &lep.mlb, "mlb/F");
  TTree_lep.Branch("RightHanded", &lep.RightHanded, "RightHanded/I");

  TTree TTree_had("TTree_had","TTree_had");
  hadronic_variables had;
  
  
  TTree_had.Branch("jj_pt", &had.jj_pt, "jj_pt/F");
  TTree_had.Branch("jj_eta", &had.jj_eta, "jj_eta/F");
  TTree_had.Branch("jj_phi", &had.jj_phi, "jj_phi/F");
  
  TTree_had.Branch("bjet_pt", &had.bjet_pt, "bjet_pt/F");
  TTree_had.Branch("bjet_eta", &had.bjet_eta, "bjet_eta/F");
  TTree_had.Branch("bjet_phi", &had.bjet_phi, "bjet_phi/F");
  
  TTree_had.Branch("met_pt", &had.met_pt, "met_pt/F");
  TTree_had.Branch("met_phi", &had.met_phi, "met_phi/F");
  TTree_had.Branch("met_eta", &had.met_eta, "met_eta/F");
  
  TTree_had.Branch("ratio", &had.ratio, "ratio/F");
  TTree_had.Branch("ratiojb", &had.ratiojb, "ratiojb/F");
  TTree_had.Branch("mjjb", &had.mjjb, "mjjb/F");
  TTree_had.Branch("mjb", &had.mjb, "mjb/F");
  TTree_had.Branch("RightHanded", &had.RightHanded, "RightHanded/I");




  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();



  // Get pointers to branches used in this analysis
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchMet = treeReader->UseBranch("MissingET");

  Int_t nleptons;
  Int_t nlept_events = 0;
  Int_t nEvents = 0;
  Int_t njet_events = 0;



  
  for(Int_t entry = 0; entry < numberOfEntries; ++entry)
  {
    treeReader->ReadEntry(entry);

    Jet *jet = nullptr;
    Jet *jet1 = nullptr;
    Jet *jet2 = nullptr;
    if(branchJet->GetEntries() > 0)
    {
      jet = (Jet*) branchJet->At(0);
      if(branchJet->GetEntries() > 2){

       jet1 = (Jet*) branchJet->At(1);
       jet2 = (Jet*) branchJet->At(2);

      }

    }

    MissingET *met = nullptr;
    if(branchMet->GetEntries() > 0)
    {
      met = (MissingET*) branchMet->At(0);
    }


    Electron *elec1 = nullptr;
    if(branchMet->GetEntries() > 0)
    {
      elec1 = (Electron *) branchElectron->At(0);
    }

    Muon *muon1 = nullptr;
    if(branchMuon->GetEntries() > 0)
    {
      muon1 = (Muon *) branchMuon->At(0);
    }

    //fill hadronic tree
    if( not(muon1 || elec1) && met && jet && jet1 && jet2 && jet->BTag+jet1->BTag+jet2->BTag > 0){

      

      Float_t values[7];
     

      if(jet->BTag > 0){
        had.bjet_pt  = jet->PT;
        had.bjet_phi =  jet->Phi;
        had.bjet_eta =  jet->Eta;
        returnJetStuff(values, jet, jet1, jet2);

      } else if (jet1->BTag > 0){
        had.bjet_pt  = jet1->PT;
        had.bjet_phi =  jet1->Phi;
        had.bjet_eta =  jet1->Eta;
        returnJetStuff(values, jet1, jet, jet2);
      } else if (jet2->BTag > 0){
        had.bjet_pt  = jet2->PT;
        had.bjet_phi =  jet2->Phi;
        had.bjet_eta =  jet2->Eta;
        returnJetStuff(values, jet2, jet, jet1 );
      }

      had.jj_pt = values[2];
      had.jj_eta = values[3];
      had.jj_phi = values[4];

      had.ratio = values[1];
      had.mjjb = values[0];
      
      had.met_pt  = met->MET;
      had.met_phi =  met->Phi;
      had.met_eta =  met->Eta;

      had.mjb =  values[5];
      had.ratiojb =  values[6];

      had.RightHanded = rightHanded;

      TTree_had.Fill();
    
    }


    

    //fill leptonic tree
    nleptons = branchElectron->GetEntries() + branchMuon->GetEntries();
    if( (muon1 || elec1) && jet && met){

      if(muon1){
        lep.lep_pt = muon1->PT;
        lep.lep_phi = muon1->Phi;
        lep.lep_eta = muon1->Eta;
      }
      if(elec1){
        lep.lep_pt = elec1->PT;
        lep.lep_phi = elec1->Phi;
        lep.lep_eta = elec1->Eta;
      }

      if(muon1 && elec1){

        if(elec1->PT > muon1->PT){
          lep.lep_pt = muon1->PT;
          lep.lep_phi = muon1->Phi;
          lep.lep_eta = muon1->Eta;
        }
        if(elec1->PT > muon1->PT){
          lep.lep_pt = elec1->PT;
          lep.lep_phi = elec1->Phi;
          lep.lep_eta = elec1->Eta;

        }
      }
    

      lep.jet_pt  = jet->PT;
      lep.jet_phi =  jet->Phi;
      lep.jet_eta =  jet->Eta;
      lep.jet_btag =  jet->BTag;

      lep.met_pt  = met->MET;
      lep.met_phi =  met->Phi;
      lep.met_eta =  met->Eta;

      lep.ratio = jet->PT/(jet->PT + lep.lep_pt);

      lep.RightHanded = rightHanded;

      TLorentzVector TL_MET;
      TL_MET.SetPtEtaPhiM(met->MET, met->Eta, met->Phi, 0 );
      TLorentzVector TL_lep;
      TL_lep.SetPtEtaPhiM(lep.lep_pt, lep.lep_eta, lep.lep_phi, 0 );
      TLorentzVector TL_b;
      TL_b.SetPtEtaPhiM(jet->PT, jet->Eta, jet->Phi, jet->Mass );

      lep.mt = (TL_MET + TL_lep + TL_b).Mt();
      lep.mlb = (TL_lep + TL_b).M();


      TTree_lep.Fill();
      nlept_events = nlept_events + 1;


    
    }
    nEvents = nEvents +1;

    if(branchJet->GetEntries() > 2){
      njet_events = njet_events + 1;
    }




    
  }


  cout << "nleptons: "<<nleptons << endl;
  cout << "nlept_events: "<<nlept_events << endl;
  cout << "nEvents: "<<nEvents << endl;
  cout << "njet_events: "<<njet_events << endl;

  TTree_lep.Write();
  TTree_had.Write();
}

