//
//  EventReader.hpp
//  selections
//
//  Created by Jeremi Niedziela on 13/02/2023.
//

#ifndef EventReader_hpp
#define EventReader_hpp

#include <stdio.h>
#include <vector>

#include <TTree.h>

#include "Event.hpp"

class EventReader {
public:
  EventReader(int _max_events=-1): max_events(_max_events){}
  
  std::vector<Event*> read_events(TTree *tree);
  
private:
  int max_events;
  
};

#endif /* EventReader_hpp */
