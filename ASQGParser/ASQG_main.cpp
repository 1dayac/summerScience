// ASQGParser.cpp : Defines the entry point for the console application.
//

#include "SGUtil.h"
#include "doppelGraph.h"
int main(int argc, char* argv[])
{
  std::string filename = argv[1];
  StringGraph* graph = SGUtil::loadASQG(filename, 0);
  doppelGraph a(graph);
  graph->writeASQG(filename + ".out");
  return 0;
}

