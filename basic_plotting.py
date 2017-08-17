from ROOT import TFile, TTree, TH1F, TH2F, TLorentzVector, TMath, TRandom, TClonesArray, TCanvas, gROOT, TGraph, TLine, TLegend
import ratioHistograms

gROOT.SetBatch(True)


f_RH_1           = TFile.Open("one_tev_RH_lep.root", "read")

f_RH_5           = TFile.Open("five_tev_RH_lep.root", "read")

f_LH_1           = TFile.Open("one_tev_LH_lep.root", "read")

f_LH_5           = TFile.Open("five_tev_LH_lep.root", "read")



RHone = f_RH_1.Get("Delphes")

RHfive = f_RH_5.Get("Delphes")


LHone = f_LH_1.Get("Delphes")

LHfive = f_LH_5.Get("Delphes")

c1 = TCanvas()

ROC_ratio = []

RHoneClass = ratioHistograms.ratioHistograms(RHone, "RHone")
LHoneClass = ratioHistograms.ratioHistograms(LHone, "LHone")

RHoneClass.drawHistograms(c1)
LHoneClass.drawHistograms(c1)

ROC_ratio.append( (ratioHistograms.makeROC(LHoneClass.TH1F_ratio, RHoneClass.TH1F_ratio, c1, "LHone", "RHone"), "1 TeV") )


#LHoneClass.makeROC(RHoneClass, c1)


RHfiveClass = ratioHistograms.ratioHistograms(RHfive, "RHfive")
LHfiveClass = ratioHistograms.ratioHistograms(LHfive, "LHfive")

RHfiveClass.drawHistograms(c1)
LHfiveClass.drawHistograms(c1)
#LHfiveClass.makeROC(RHfiveClass, c1)


ROC_ratio.append( (ratioHistograms.makeROC(LHfiveClass.TH1F_ratio, RHfiveClass.TH1F_ratio, c1, "LHfive", "RHfive"), "5 TeV") )


ratioHistograms.ROCMGDraw(ROC_ratio, c1)

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