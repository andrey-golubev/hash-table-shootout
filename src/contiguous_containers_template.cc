#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <algorithm>
#include <random>
#include <fstream>
#include <iostream>
#include <chrono>
#include <array>

// TODO When generating random values to insert in the map there is no check
// to see if duplicate random values are generated. Could improve that (but the probability is so so
// low and the impact nearly null that it's not really worth it).

static const std::array<char, 62> ALPHANUMERIC_CHARS = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
};

#ifndef LOAD_FACTOR  // QList 5.15 defines
#define LOAD_FACTOR(container) (container.capacity() == 0 ? 0.0 : double(container.size()) / double(container.capacity()))
#endif

/**
 * SMALL_STRING_SIZE should be small enough so that there is no heap allocation when a std::string is created.
 */
static const std::size_t SMALL_STRING_SIZE = 15;
static const std::size_t STRING_SIZE = 50;

static const std::int64_t SEED = 0;
static std::mt19937_64 generator(SEED);


std::size_t get_memory_usage_bytes() {
    std::ifstream file("/proc/self/statm");

    std::size_t memory;
    file >> memory; // Ignore first
    file >> memory;

    return memory * getpagesize();
}

std::string get_random_alphanum_string(std::size_t size) {
    std::uniform_int_distribution<std::size_t> rd_uniform(0, ALPHANUMERIC_CHARS.size() - 1);

    std::string str(size, '\0');
    for(std::size_t i = 0; i < size; i++) {
        str[i] = ALPHANUMERIC_CHARS[rd_uniform(generator)];
    }

    return str;
}

/**
 * Generate a vector [0, nb_ints) and shuffle it
 */
std::vector<std::int64_t> get_random_shuffle_range_ints(std::size_t nb_ints) {
    std::vector<std::int64_t> random_shuffle_ints(nb_ints);
    std::iota(random_shuffle_ints.begin(), random_shuffle_ints.end(), 0);
    std::shuffle(random_shuffle_ints.begin(), random_shuffle_ints.end(), generator);

    return random_shuffle_ints;
}

/**
 * Generate random vector of random ints between min and max.
 */
std::vector<std::int64_t> get_random_full_ints(std::size_t nb_ints,
                                               std::int64_t min = 0,
                                               std::int64_t max = std::numeric_limits<std::int64_t>::max())
{
    std::uniform_int_distribution<std::int64_t> rd_uniform(min, max);

    std::vector<std::int64_t> random_ints(nb_ints);
    for(std::size_t i = 0; i < random_ints.size(); i++) {
        random_ints[i] = rd_uniform(generator);
    }

    return random_ints;
}


std::vector<std::string> get_random_alphanum_strings(std::size_t nb_strings, std::size_t string_size) {
    std::vector<std::string> random_strings(nb_strings);
    for(std::size_t i = 0; i < random_strings.size(); i++) {
        random_strings[i] = get_random_alphanum_string(string_size);
    }

    return random_strings;
}

class measurements {
public:
    measurements(): m_memory_usage_bytes_start(get_memory_usage_bytes()),
                    m_chrono_start(std::chrono::high_resolution_clock::now())

    {
    }

    ~measurements() {
        const auto chrono_end = std::chrono::high_resolution_clock::now();
        const std::size_t memory_usage_bytes_end = get_memory_usage_bytes();

        const double nb_seconds = std::chrono::duration<double>(chrono_end - m_chrono_start).count();
        // On reads or delete the used bytes could be less than initially.
        const std::size_t used_memory_bytes = (memory_usage_bytes_end > m_memory_usage_bytes_start)?
                                                    memory_usage_bytes_end - m_memory_usage_bytes_start:0;

        std::cout << nb_seconds << " " << used_memory_bytes << " ";
    }

private:
    std::size_t m_memory_usage_bytes_start;
    std::chrono::time_point<std::chrono::high_resolution_clock> m_chrono_start;
};


int main(int argc, char ** argv) {
    if(argc != 3) {
        std::cout << argv[0] << " num_keys test_type" << std::endl;
        return 1;
    }

    const std::int64_t num_keys = std::stoll(argv[1]);
    const std::string test_type = argv[2];
    const std::int64_t value = 1;

    const auto append = [&] (auto &container, auto value) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            APPEND(container, value);
        }
    };

    const auto prepend = [&] (auto &container, auto value) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            PREPEND(container, value);
        }
    };

    const auto insert1_mid = [&] (auto &container, auto value) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            INSERT_1(container, container.size() / 2, value);
        }
    };

    const auto insert1_quarter = [&] (auto &container, auto value) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            INSERT_1(container, container.size() / 4, value);
        }
    };

    const auto insert1_last_quarter = [&] (auto &container, auto value) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            INSERT_1(container, 3 * container.size() / 4, value);
        }
    };

    const auto access_every = [&] (auto &container, auto expected) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            auto value = ACCESS(container, i);
            if (value != expected) { printf("error"); exit(4); }
        }
    };

    const auto remove_mid = [&] (auto &container) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            REMOVE(container, container.size() / 2);
        }
    };

    const auto remove_last = [&] (auto &container) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            REMOVE(container, container.size() - 1);
        }
    };

    const auto remove_first = [&] (auto &container) {
        measurements m;
        for(std::int64_t i = 0; i < num_keys; i++) {
            REMOVE(container, 0);
        }
    };

    const auto append_suffix = [] (std::string workload, const std::string& suffix) {
        workload += suffix;
        return workload;
    };

    const auto parse_and_run = [&] (auto &container, auto value, std::string suffix) {
        if(test_type == append_suffix("append_", suffix)) {
            append(container, value);
            return true;
        }
        else if(test_type == append_suffix("prepend_", suffix)) {
            prepend(container, value);
            return true;
        }
        else if(test_type == append_suffix("insert1_mid_", suffix)) {
            insert1_mid(container, value);
            return true;
        }
        else if(test_type == append_suffix("insert1_quarter_", suffix)) {
            insert1_quarter(container, value);
            return true;
        }
        else if(test_type == append_suffix("insert1_last_quarter_", suffix)) {
            insert1_last_quarter(container, value);
            return true;
        }
        else if(test_type == append_suffix("access_every_", suffix)) {
            auto copy = container;
            CLEAN_RESIZE(copy, num_keys);
            access_every(copy, value);
            return true;
        }
        else if(test_type == append_suffix("remove_first_", suffix)) {
            auto copy = container;
            CLEAN_RESIZE(copy, num_keys + 1);
            remove_first(copy);
            return true;
        }
        else if(test_type == append_suffix("remove_mid_", suffix)) {
            auto copy = container;
            CLEAN_RESIZE(copy, num_keys + 1);
            remove_mid(copy);
            return true;
        }
        else if(test_type == append_suffix("remove_last_", suffix)) {
            auto copy = container;
            CLEAN_RESIZE(copy, num_keys + 1);
            remove_last(copy);
            return true;
        }
        else {
            return false;
        }
    };


    SETUP

    bool parsed = false;
    parsed |= parse_and_run(container, int{}, "int");
    parsed |= parse_and_run(qstr_container, QString{}, "qstr");
    parsed |= parse_and_run(stdstr_container, std::string{}, "stdstr");
    parsed |= parse_and_run(three_ptrs_container, ThreePtrs{}, "three_ptrs");

    if (!parsed) {
        std::cout << "Unknown test type: " << test_type << "." << std::endl;
        std::exit(1);
    }

    // ratio of size to capacity:
    const double load_factor = std::max({
        LOAD_FACTOR(container), LOAD_FACTOR(qstr_container),
        LOAD_FACTOR(stdstr_container), LOAD_FACTOR(three_ptrs_container)
    });
    std::cout << load_factor << std::endl;

    return 0;
}
