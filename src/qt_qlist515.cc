#include "custom_structs.h"

#include <inttypes.h>
#include <string>

#include <QtCore/QString>
#include <QtCore/QList>
#include <QtCore/QVector>

typedef QList<int> container_t;
typedef QList<QString> qstr_container_t;
typedef QList<std::string> stdstr_container_t;
typedef QList<ThreePtrs> three_ptrs_container_t;

#define SETUP container_t container; qstr_container_t qstr_container; \
              stdstr_container_t stdstr_container; three_ptrs_container_t three_ptrs_container;

#define APPEND(container, val) container.append(val);
#define PREPEND(container, val) container.prepend(val);
#define INSERT_1(container, pos, val) container.insert((pos), val);
#define REMOVE(container, pos) container.erase(container.begin() + (pos));
#define CLEAN_RESIZE(container, size) { container = QVector<typename decltype(container)::value_type>(int(size)).toList(); }

#define LOAD_FACTOR(...) 0.0

#include "contiguous_containers_template.cc"
