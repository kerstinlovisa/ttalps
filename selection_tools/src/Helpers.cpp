#include "Helpers.hpp"

template <typename T>
std::string to_string_with_precision(const T a_value, const int n)
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

std::string to_nice_string(double a_value, int precision)
{
  std::string result = to_string_with_precision(a_value, precision);
  result = replace_all(result, ".", "p");
  return result;
}