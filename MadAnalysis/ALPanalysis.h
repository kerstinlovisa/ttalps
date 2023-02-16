#ifndef analysis_ALPanalysis_h
#define analysis_ALPanalysis_h

#include "SampleAnalyzer/Process/Analyzer/AnalyzerBase.h"

namespace MA5
{
class ALPanalysis : public AnalyzerBase
{
  INIT_ANALYSIS(ALPanalysis,"ALPanalysis")

 public:
  virtual bool Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters);
  virtual void Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files);
  virtual bool Execute(SampleFormat& sample, const EventFormat& event);
  std::string data(MCParticleFormat part);
  void buildOutput(MCParticleFormat& mother, int& n, int& count, std::string& tobebuilt);
  bool hasTopAncestor(MCParticleFormat part);
  std::vector<MCParticleFormat> findAncestorLine(MCParticleFormat part, std::vector<MCParticleFormat> line);
  MCParticleFormat jetAncestor(MCParticleFormat part);
 private:
};
}

#endif
