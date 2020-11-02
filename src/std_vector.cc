#include "custom_structs.h"

#include <inttypes.h>
#include <string>
#include <vector>

#include <QtCore/QString>

typedef std::vector<int> container_t;
typedef std::vector<QString> qstr_container_t;
typedef std::vector<std::string> stdstr_container_t;
typedef std::vector<ThreePtrs> three_ptrs_container_t;

#define SETUP container_t container; qstr_container_t qstr_container; \
              stdstr_container_t stdstr_container; three_ptrs_container_t three_ptrs_container;

#define APPEND(container, val) container.push_back(val);
#define PREPEND(container, val) container.insert(container.begin(), val);
#define INSERT_1(container, pos, val) container.insert(container.begin() + (pos), val);
#define REMOVE(container, pos) container.erase(container.begin() + (pos));
#define ACCESS(container, pos) container[(pos)];
#define CLEAN_RESIZE(container, size) { container.clear(); container.resize(size); }


#include "contiguous_containers_template.cc"
