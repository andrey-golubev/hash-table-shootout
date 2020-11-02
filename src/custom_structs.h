#pragma once

struct ThreePtrs {
    void *one = nullptr;
    void *two = nullptr;
    void *three = nullptr;

private:
    friend bool operator==(const ThreePtrs& a, const ThreePtrs& b) {
        return a.one == b.one && a.two == b.two && a.three == b.three;
    }

    friend bool operator!=(const ThreePtrs& a, const ThreePtrs& b) {
        return !(a == b);
    }
};
