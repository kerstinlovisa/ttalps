//
//  Helpers.hpp
//  selections
//
//  Created by Jeremi Niedziela on 04/04/2023.
//

#ifndef Helpers_h
#define Helpers_h

#include <ostream>
#include <sstream>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <tuple>
#include <memory>
#include <algorithm>

#pragma clang diagnostic push // save the current state
#pragma clang diagnostic ignored "-Wdocumentation" // turn off ROOT's warnings
#pragma clang diagnostic ignored "-Wconversion"

#include "TH1D.h"
#include "TH2D.h"
#include "TGraph.h"
#include "TGraphAsymmErrors.h"
#include "TF1.h"
#include "TTree.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TLegend.h"

#pragma clang diagnostic pop // restores the saved state for diagnostics

template <typename T>
std::string to_string_with_precision(const T a_value, const int n = 6)
{
  std::ostringstream out;
  out.precision(n);
  out << std::fixed << a_value;
  return out.str();
}

std::string replace_all(std::string str, const std::string& from, const std::string& to) {
  size_t start_pos = 0;
  while((start_pos = str.find(from, start_pos)) != std::string::npos) {
    str.replace(start_pos, from.length(), to);
    start_pos += to.length(); // Handles case where 'to' is a substring of 'from'
  }
  return str;
}

std::string to_nice_string(double a_value, int precision = 1)
{
  std::string result = to_string_with_precision(a_value, precision);
  result = replace_all(result, ".", "p");
  return result;
}

#endif /* Helpers_h */
