#include "SGUtil.h"
#include <hash_map>
//monotization of bidirected graph
//and Dinic algorithm on it
struct doppelGraph
{
public:
  doppelGraph();
  doppelGraph(StringGraph* graph);
private:
  std::vector<std::vector<int>> incidenceMatrix;
  std::vector<std::vector<int>> flowMatrix;
  std::hash_map<int, std::string> vertexLabels;
  std::hash_map<std::string, int> reverseVertexLabels;

  
};