#ifndef analysis_ttalp_h
#define analysis_ttalp_h

#include "SampleAnalyzer/Process/Analyzer/AnalyzerBase.h"

namespace MA5
{
class ttalp : public AnalyzerBase
{
  INIT_ANALYSIS(ttalp,"ttalp")

 public:
  virtual bool Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters);
  virtual void Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files);
  virtual bool Execute(SampleFormat& sample, const EventFormat& event);
  std::string data(MCParticleFormat part);
 private:
};
}

#endif
