from ROOT import TFile, TTree, TH1F, TLorentzVector, TMath, TRandom, TClonesArray, TCanvas, gROOT
from root_numpy import tree2array
from histogrammar import *
import numpy

gROOT.SetBatch(True)


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



class ratioHistograms:
	def __init__(self, tree, name):
		self.name = name
		self.TH1F_ratio = TH1F("TH1F_ratio_{}".format(name), "TH1F_ratio; E(b)/E(t); count", 10, 0 , 1)
		self.TH1F_pt = TH1F("TH1F_pt{}".format(name), "TH1F_pt{}".format(name), 10, 0, 2000)

		self.fillHistogram(tree)



	def fillHistogram(self,tree):
	
		for count in range(tree.GetEntries()):
			muon_pt = 0
			electron_pt = 0
			jet_pt = 0
		
			tree.GetEntry(count)
			jets = getJets(tree)
			muons = getMuons(tree)
			electrons = getElectrons(tree)
		
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
				#print jet_pt/(jet_pt+muon_pt)
				self.TH1F_ratio.Fill(jet_pt/(jet_pt+muon_pt))
				self.TH1F_pt.Fill(muon_pt)
			elif electron_pt*jet_pt > 0:
				#print jet_pt/(jet_pt+electron_pt)
				self.TH1F_ratio.Fill(jet_pt/(jet_pt+electron_pt))
				self.TH1F_pt.Fill(electron_pt)
		 
		
		#hist = {'TH1F_ratio':self.TH1F_ratio, 'TH1F_pt':TH1F_pt}
		#return hist

	def drawHistogram(self, fillHistogramClass):
		self.TH1F_ratio.SetLineColor(2)
		self.TH1F_ratio.Draw()
		fillHistogramClass.TH1F_ratio.SetLineColor(3)
		fillHistogramClass.TH1F_ratio.Draw("same")
		c1.SaveAs("ratio_{}_{}.png".format(self.name, fillHistogramClass.name))




RHoneClass = ratioHistograms(RHone, "RHone")
LHoneClass = ratioHistograms(LHone, "LHone")

LHoneClass.drawHistogram(RHoneClass)









#Bundle = UntypedLabel
#
#RH_one_array = tree2array(RHone,
#	 branches=[	'Muon.PT[0]', 'Jet.PT[0]' , 
#	 			'Jet.PT[0]/(Muon.PT[0] + Jet.PT[0])'],
#    selection='Muon.PT[0] > 10',
#    start=0, stop=-1, step=1)
#
#
#RH_one_array.dtype.names = [	'muonPt', 'leadingJetPt', 
#						'ratio'  ]
#
#
#print RH_one_array
#
#standard_histograms = Select( lambda array: numpy.logical_and(array['muonPt'] > 10 ,abs(array['leadingJetPt']) > 10), Bundle(
#
#
#D1_ratio = Bin(	100, 0, 1, 
#	lambda array : (array['ratio'], Count() )),
#
#))
#
#standard_histograms.fill.numpy(RH_one_array)
#
#TH1D_ratio = standard_histograms.get("D1_ratio").plot.root("D1_ratio", "ratio")
#
#TH1D_ratio.Draw()
#c1.SaveAs("TH1D_ratio.png")#