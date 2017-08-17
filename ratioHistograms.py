from ROOT import TFile, TTree, TH1F, TH2F, TLorentzVector, TMath, TRandom, TClonesArray, TCanvas, gROOT, TGraph, TLine, TLegend, TMultiGraph
import math

def getMuons(tree):
	nMuons = tree.GetLeaf('Muon_size').GetValue()
	Muons=[]
	for j in range(int(nMuons)):
			pt = tree.GetLeaf('Muon.PT').GetValue(j)
			eta = tree.GetLeaf('Muon.Eta').GetValue(j)
			phi= tree.GetLeaf('Muon.Phi').GetValue(j)
			mass = .106
		
			cand={'pt':pt, 'eta':eta, 'phi':phi,'mass':mass}
			Muons.append(cand)
	return Muons

def getElectrons(tree):
	nElectrons = tree.GetLeaf('Electron_size').GetValue()
	Electrons=[]
	for j in range(int(nElectrons)):
			pt = tree.GetLeaf('Electron.PT').GetValue(j)
			eta = tree.GetLeaf('Electron.Eta').GetValue(j)
			phi= tree.GetLeaf('Electron.Phi').GetValue(j)
			mass = .000511
		
			cand={'pt':pt, 'eta':eta, 'phi':phi,'mass':mass}
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

def getMissingET(tree):
	nMissingET = tree.GetLeaf('MissingET_size').GetValue()
	MissingET=[]
	for j in range(int(nMissingET)):
			MET = tree.GetLeaf('MissingET.MET').GetValue(j)
			eta = tree.GetLeaf('MissingET.Eta').GetValue(j)
			phi= tree.GetLeaf('MissingET.Phi').GetValue(j)

			cand={'MET':MET, 'eta':eta, 'phi':phi}
			MissingET.append(cand)
	return MissingET



class ratioHistograms:
	def __init__(self, tree, name):
		self.name = name
		self.nBins = 20
		self.TH1F_ratio = TH1F("TH1F_ratio_{}".format(name), "TH1F_ratio; E(b)/E(t); count", self.nBins, 0 , 1)
		self.TH1F_pt = TH1F("TH1F_pt{}".format(name), "TH1F_pt{}".format(name), self.nBins, 0, 2000)
		self.TH1F_deltaR_MET_b = TH1F("TH1F_deltaR_MET_b{}".format(name), "TH1F_deltaR_MET_b{}".format(name), self.nBins, 0, 6)
		self.TH1F_deltaR_MET_l = TH1F("TH1F_deltaR_MET_l{}".format(name), "TH1F_deltaR_MET_l{}".format(name), self.nBins, 0, 6)
		self.TH1F_deltaR_b_l = TH1F("TH1F_deltaR_b_l{}".format(name), "TH1F_deltaR_b_l{}".format(name), self.nBins, 0, 6)
		self.TH1F_deltaPhi_MET_b = TH1F("TH1F_deltaPhi_MET_b{}".format(name), "TH1F_deltaPhi_MET_b{}".format(name), self.nBins, -4, 4)
		self.TH1F_deltaPhi_MET_l = TH1F("TH1F_deltaPhi_MET_l{}".format(name), "TH1F_deltaPhi_MET_l{}".format(name), self.nBins, -4, 4)
		self.TH1F_deltaPhi_b_l = TH1F("TH1F_deltaPhi_b_l{}".format(name), "TH1F_deltaPhi_b_l{}".format(name), self.nBins, -4, 4)


		self.fillHistogram(tree)
		self.TH1F_ratio.Scale(1.0/(self.TH1F_ratio.GetEntries() + 0.0))

	def drawHistograms(self,c1):

		self.TH1F_ratio.Draw()
		c1.SaveAs("output/TH1F_ratio_{}.png".format(self.name))
		self.TH1F_pt.Draw()
		c1.SaveAs("output/TH1F_pt_{}.png".format(self.name))
		self.TH1F_deltaR_MET_b.Draw()
		c1.SaveAs("output/TH1F_deltaR_MET_b_{}.png".format(self.name))
		self.TH1F_deltaR_MET_l.Draw()
		c1.SaveAs("output/TH1F_deltaR_MET_l_{}.png".format(self.name))
		self.TH1F_deltaR_b_l.Draw()
		c1.SaveAs("output/TH1F_deltaR_b_l_{}.png".format(self.name))
		self.TH1F_deltaPhi_MET_b.Draw()
		c1.SaveAs("output/TH1F_deltaPhi_MET_b_{}.png".format(self.name))
		self.TH1F_deltaPhi_MET_l.Draw()
		c1.SaveAs("output/TH1F_deltaPhi_MET_l_{}.png".format(self.name))
		self.TH1F_deltaPhi_b_l.Draw()
		c1.SaveAs("output/TH1F_deltaPhi_b_l_{}.png".format(self.name))


	def fillHistogram(self,tree):
	
		for count in range(tree.GetEntries()):
			muon_pt = 0
			electron_pt = 0
			jet_pt = 0
			lep_pt = 0
			met_pt = 0

			tree.GetEntry(count)
			jets = getJets(tree)
			muons = getMuons(tree)
			electrons = getElectrons(tree)
			METs = getMissingET(tree)
		
			jetTL  = TLorentzVector()
			leptonTL = TLorentzVector()
			METTL = TLorentzVector()

			for jet in jets:
				if jet['btag'] == 1:
					#print count, jet['pt'], jet['btag']
					jet_pt = jet['pt']
					jetTL.SetPtEtaPhiM(jet['pt'],jet['eta'],jet['phi'],jet['mass'])
					
					break

			for met in METs:
					METTL.SetPtEtaPhiM(met['MET'],met['eta'],met['phi'],0)
					met_pt = met['MET']
					break
		
			for muon in muons:
				#print count, muon['pt']
				muon_pt = muon['pt']
				lep_pt = muon['pt']
				leptonTL.SetPtEtaPhiM(muon['pt'],muon['eta'],muon['phi'],muon['mass'])
				break
		
			for electron in electrons:
				#print count, electron['pt']
				electron_pt = electron['pt']
				if muon_pt > 0 and electron_pt > muon_pt:
					lep_pt =  electron['pt']
					leptonTL.SetPtEtaPhiM(muon['pt'],muon['eta'],muon['phi'],muon['mass'])
				break


		
			if lep_pt*jet_pt > 0:
				#print jet_pt/(jet_pt+muon_pt)
				self.TH1F_ratio.Fill(jet_pt/(jet_pt+lep_pt))
				self.TH1F_pt.Fill(met_pt)
			#elif electron_pt*jet_pt > 0:
				#print jet_pt/(jet_pt+electron_pt)
			#	self.TH1F_ratio.Fill(jet_pt/(jet_pt+electron_pt))
			#	self.TH1F_pt.Fill(electron_pt)

			if jet_pt*met_pt*lep_pt:
				self.TH1F_deltaR_MET_b.Fill(jetTL.DeltaR(METTL))
				self.TH1F_deltaR_MET_l.Fill(leptonTL.DeltaR(METTL))
				self.TH1F_deltaR_b_l.Fill(leptonTL.DeltaR(jetTL))
				self.TH1F_deltaPhi_MET_b.Fill(jetTL.DeltaPhi(METTL))
				self.TH1F_deltaPhi_MET_l.Fill(leptonTL.DeltaPhi(METTL))
				self.TH1F_deltaPhi_b_l.Fill(leptonTL.DeltaPhi(jetTL))
		
		#hist = {'TH1F_ratio':self.TH1F_ratio, 'TH1F_pt':TH1F_pt}
		#return hist

	def makeROC(self, fillHistogramClass, c1):
		self.TH1F_ratio.SetLineColor(2)
		self.TH1F_ratio.Draw()
		fillHistogramClass.TH1F_ratio.SetLineColor(3)
		fillHistogramClass.TH1F_ratio.Draw("same")
		c1.SaveAs("output/ratio_{}_{}.png".format(self.name, fillHistogramClass.name))

		#TGraph_ROC = TGraph("roc_{}_{}".format(self.name, fillHistogramClass.name), "roc_{}_{}".format(self.name, fillHistogramClass.name), )
		integralSelf = self.TH1F_ratio.GetIntegral()
		integralExternal = fillHistogramClass.TH1F_ratio.GetIntegral()
		if (len(integralSelf) == len(integralExternal)):

			for i in range(self.nBins):
				binCount =  i +1
			#	print self.TH1F_ratio.GetXaxis().GetBinCenter(binCount)
			#	#print fillHistogramClass.TH1F_ratio.GetXaxis().GetBinCenter(binCount)
				print "self", integralSelf[binCount]
				print "external", integralExternal[binCount]

			c1.Clear()
			yEqualsX = TLine(0,0, 1,1)
			yEqualsX.SetLineStyle(7)
			TGraph_ROC = TGraph( self.nBins + 1, integralSelf,  integralExternal)
			TGraph_ROC.Draw()
			yEqualsX.Draw()
			c1.SaveAs("output/ROC_{}_{}.png".format(self.name, fillHistogramClass.name))

			AOC = TGraph_ROC.Integral(0, -1) +.5
			print " AOC ROC between {} and {}: {}".format(self.name, fillHistogramClass.name, AOC)
				
		else:
			print "not same length hists"


def makeROC(hist1, hist2, c1, name1, name2):
	hist1.SetLineColor(2)
	hist1.Draw()
	hist2.SetLineColor(3)
	hist2.Draw("same")
	c1.SaveAs("output/ratio_{}_{}.png".format(name1, name2))

	#TGraph_ROC = TGraph("roc_{}_{}".format(self.name, fillHistogramClass.name), "roc_{}_{}".format(self.name, fillHistogramClass.name), )
	integralSelf = hist1.GetIntegral()
	integralExternal = hist2.GetIntegral()

	nBins = hist1.GetNbinsX()
	if (len(integralSelf) == len(integralExternal)):

		for i in range(nBins):
			binCount =  i +1
		#	print hist1.GetXaxis().GetBinCenter(binCount)
		#	#print hist2.GetXaxis().GetBinCenter(binCount)
			print "self", integralSelf[binCount]
			print "external", integralExternal[binCount]

		c1.Clear()
		yEqualsX = TLine(0,0, 1,1)
		yEqualsX.SetLineStyle(7)

		TGraph_ROC = TGraph( nBins + 1, integralSelf,  integralExternal)
		TGraph_ROC.GetHistogram().SetTitle("ROC curve between {} and {}".format(name1, name2))
		TGraph_ROC.Draw()
		yEqualsX.Draw()
		c1.SaveAs("output/ROC_{}_{}.png".format(name1, name2))

		AOC = TGraph_ROC.Integral(0, -1) +.5
		print " AOC ROC between {} and {}: {}".format(name1, name2, AOC)
		return TGraph_ROC
			
	else:
		print "not same length hists"

	

def ROCMGDraw(TGraphArray, c1):
	c1.Clear()
	colorArray = [1,2,3,4,6,7]
	AOC = 0
	leg = TLegend(0.1,0.7,0.48,0.9)
	mg = TMultiGraph()
	title_text = []
	l_count = 0

	for TGraphInstance, title in TGraphArray:
		print TGraphInstance, title
		TGraphInstance.SetLineColor(colorArray[l_count])
		mg.Add(TGraphInstance)
		AOC = TGraphInstance.Integral(0, -1) +.5 
		leg.AddEntry(TGraphInstance, "{} AOC: {}".format(title, AOC))
		title_text.append(title)

		l_count = l_count +1

	title_text = "_".join(title_text)
	
	yEqualsX = TLine(0,0, 1,1)
	yEqualsX.SetLineStyle(7)
	
	TH2F_range = TH2F("range_{}".format(title_text), "range_{}".format(title_text), 10, 0, 1, 10, 0, 1)
	TH2F_range.Draw()
	mg.Draw("AL")
	leg.Draw("L")
	yEqualsX.Draw()
	title_text = title_text.replace(" ", "_")
	

	c1.SaveAs("output/ROC_{}.png".format(title_text))	
	c1.Clear()