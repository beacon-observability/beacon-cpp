// SPDX-License-Identifier: Apache-2.0
#include <array>
#include <chrono>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include "opentelemetry/exporters/otlp/otlp_http_exporter_factory.h"
#include "opentelemetry/exporters/otlp/otlp_http_exporter_options.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/sdk/trace/batch_span_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"

namespace otlp = opentelemetry::exporter::otlp;
namespace sdk = opentelemetry::sdk::trace;

int main(int argc, char **argv)
{
  if (argc != 2 && argc != 3) {
    std::cerr << "usage: beacon_cpp_otlp TRACE_URL [--expect-failure]\n";
    return 2;
  }
  const bool failure = argc == 3 && std::string(argv[2]) == "--expect-failure";
  if (argc == 3 && !failure) return 2;
  otlp::OtlpHttpExporterOptions options;
  options.url = argv[1];
  options.content_type = otlp::HttpRequestContentType::kBinary;
  options.timeout = std::chrono::milliseconds(500);
  options.retry_policy_max_attempts = 1;
  auto exporter = otlp::OtlpHttpExporterFactory::Create(options);
  if (failure) {
    auto record = exporter->MakeRecordable();
    record->SetName("beacon-cpp-rejected");
    const auto start = std::chrono::steady_clock::now();
    const auto result = exporter->Export({&record, 1});
    const auto elapsed = std::chrono::steady_clock::now() - start;
    exporter->Shutdown(std::chrono::seconds(1));
    if (result != opentelemetry::sdk::common::ExportResult::kFailure ||
        elapsed > std::chrono::seconds(5)) return 1;
    std::cout << "{\"export_failed\":true,\"bounded\":true}\n";
    return 0;
  }
  sdk::BatchSpanProcessorOptions batch;
  batch.schedule_delay_millis = std::chrono::seconds(60);
  auto processor = sdk::BatchSpanProcessorFactory::Create(std::move(exporter), batch);
  auto resource = opentelemetry::sdk::resource::Resource::Create(
      {{"service.name", "beacon-cpp-acceptance"}, {"service.version", "0.1.0"}});
  auto provider = sdk::TracerProviderFactory::Create(std::move(processor), resource);
  auto tracer = provider->GetTracer("beacon-cpp-acceptance", "0.1.0");
  auto root = tracer->StartSpan("request");
  opentelemetry::trace::StartSpanOptions child_options;
  child_options.parent = root->GetContext();
  auto child = tracer->StartSpan("work", child_options);
  child->SetAttribute("beacon.acceptance", true);
  child->End();
  auto final = tracer->StartSpan("exit-final", child_options);
  final->End();
  std::array<char,32> trace_id{};
  std::array<char,16> root_id{};
  root->GetContext().trace_id().ToLowerBase16(trace_id);
  root->GetContext().span_id().ToLowerBase16(root_id);
  root->End();
  const bool shutdown = provider->Shutdown(std::chrono::seconds(5));
  std::cout << "{\"trace_id\":\"" << std::string(trace_id.data(), trace_id.size())
            << "\",\"root_span_id\":\"" << std::string(root_id.data(), root_id.size())
            << "\",\"shutdown_ok\":" << (shutdown ? "true" : "false") << "}\n";
  return shutdown ? 0 : 1;
}
