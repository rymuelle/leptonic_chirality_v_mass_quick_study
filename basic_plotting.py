from ROOT import TFile, TTree, TH1F, TLorentzVector, TMath, TRandom, TClonesArray, TCanvas
from root_numpy import tree2array


f_RH_1           = TFile.Open("one_tev_RH_lep.root", "read")

f_RH_5           = TFile.Open("five_tev_LH_lep.root", "read")

f_LH_1           = TFile.Open("one_tev_LH_lep.root", "read")

f_LH_5           = TFile.Open("five_tev_RH_lep.root", "read")



RHone = f_RH_1.Get("Delphes")

RHfive = f_RH_5.Get("Delphes")


LHone = f_LH_1.Get("Delphes")

LHfive = f_LH_5.Get("Delphes")

c1 = TCanvas()


def getMuons(tree):
	nMuons = tree.GetLeaf('Muon_size').GetValue()
	Muons=[]
	for j in range(int(nMuons)):
			pt = tree.GetLeaf('Muon.PT').GetValue(j)
			eta = tree.GetLeaf('Muon.Eta').GetValue(j)
			phi= tree.GetLeaf('Muon.Phi').GetValue(j)
			
		
			cand={'pt':pt, 'eta':eta, 'phi':phi,}
			Muons.append(cand)
	return Muons

def getElectrons(tree):
	nElectrons = tree.GetLeaf('Electron_size').GetValue()
	Electrons=[]
	for j in range(int(nElectrons)):
			pt = tree.GetLeaf('Electron.PT').GetValue(j)
			eta = tree.GetLeaf('Electron.Eta').GetValue(j)
			phi= tree.GetLeaf('Electron.Phi').GetValue(j)
			
		
			cand={'pt':pt, 'eta':eta, 'phi':phi,}
			Electrons.append(cand)
	return Electrons


def getJets(tree):
	nJets = tree.GetLeaf('Jet_size').GetValue()
	Jets=[]
	for j in range(int(nJets)):
			pt = tree.GetLeaf('Jet.PT').GetValue(j)
			eta = tree.GetLeaf('Jet.Eta').GetValue(j)
			phi= tree.GetLeaf('Jet.Phi').GetValue(j)
			mass = tree.GetLeaf('Jet.Mass').GetValue(j)
			btag = tree.GetLeaf('Jet.BTag').GetValue(j)
		
			cand={'pt':pt, 'eta':eta, 'phi':phi,'mass':mass, 'btag':btag}
			Jets.append(cand)
	return Jets

def returnHistogram(test, name):
	TH1F_ratio = TH1F("TH1F_ratio_{}".format(name), "TH1F_ratio_{}".format(name), 10, 0, 1)
	TH1F_pt = TH1F("TH1F_pt{}".format(name), "TH1F_pt{}".format(name), 10, 0, 2000)

	for count in range(test.GetEntries()):
		muon_pt = 0
		electron_pt = 0
		jet_pt = 0
	
		test.GetEntry(count)
		jets = getJets(test)
		muons = getMuons(test)
		electrons = getElectrons(test)
	
		for jet in jets:
			if jet['btag'] == 1:
				#print count, jet['pt'], jet['btag']
				jet_pt = jet['pt']
				break
	
		for muon in muons:
			#print count, muon['pt']
			muon_pt = muon['pt']
			break
	
		for electron in electrons:
			#print count, electron['pt']
			electron_pt = electron['pt']
			break
	
		if muon_pt*jet_pt > 0:
			print jet_pt/(jet_pt+muon_pt)
			TH1F_ratio.Fill(jet_pt/(jet_pt+muon_pt))
			TH1F_pt.Fill(muon_pt)
		elif electron_pt*jet_pt > 0:
			print jet_pt/(jet_pt+electron_pt)
			TH1F_ratio.Fill(jet_pt/(jet_pt+electron_pt))
			TH1F_pt.Fill(electron_pt)
	 
	hist = {'TH1F_ratio':TH1F_ratio, 'TH1F_pt':TH1F_pt}
	return hist




one_tev_RH = returnHistogram(RHone, "1TeV")
five_tev_RH = returnHistogram(RHfive, "5TeV")


one_tev_LH = returnHistogram(LHone, "1TeV")
five_tev_LH = returnHistogram(LHfive, "5TeV")


one_tev_RH['TH1F_ratio'].Scale(1.0/one_tev_RH['TH1F_ratio'].GetEntries())
one_tev_RH['TH1F_ratio'].Draw()
five_tev_RH['TH1F_ratio'].Scale(1.0/five_tev_RH['TH1F_ratio'].GetEntries())
five_tev_RH['TH1F_ratio'].SetLineColor(2)
five_tev_RH['TH1F_ratio'].Draw("same")

five_tev_LH['TH1F_ratio'].Scale(1.0/five_tev_LH['TH1F_ratio'].GetEntries())
five_tev_LH['TH1F_ratio'].SetLineColor(4)
five_tev_LH['TH1F_ratio'].Draw("same")

one_tev_LH['TH1F_ratio'].Scale(1.0/one_tev_LH['TH1F_ratio'].GetEntries())
one_tev_LH['TH1F_ratio'].SetLineColor(3)
one_tev_LH['TH1F_ratio'].Draw("same")


c1.SaveAs("one_tev.png")




#one_tev['TH1F_pt'].Scale(1.0/one_tev['TH1F_pt'].GetEntries())
#one_tev['TH1F_pt'].Draw()
#five_tev['TH1F_pt'].SetLineColor(2)
#five_tev['TH1F_pt'].Scale(1.0/five_tev['TH1F_pt'].GetEntries())
#five_tev['TH1F_pt'].Draw("same")
#c1.SaveAs("pt.png")




		