#include "custom_structs.h"

#include <inttypes.h>
#include <string>

#include <QtCore/QString>
#include <QtCore/QVector>

typedef QVector<int> container_t;
typedef QVector<QString> qstr_container_t;
typedef QVector<std::string> stdstr_container_t;
typedef QVector<ThreePtrs> three_ptrs_container_t;

#define SETUP container_t container; qstr_container_t qstr_container; \
              stdstr_container_t stdstr_container; three_ptrs_container_t three_ptrs_container;

#define APPEND(container, val) container.append(val);
#define PREPEND(container, val) container.prepend(val);
#define INSERT_1(container, pos, val) container.insert((pos), val);
#define REMOVE(container, pos) container.remove((pos));


#include "contiguous_containers_template.cc"
