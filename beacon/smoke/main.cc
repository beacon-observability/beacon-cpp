// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <utility>
#include "opentelemetry/exporters/ostream/span_exporter_factory.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"

int main()
{
  namespace sdk = opentelemetry::sdk::trace;
  auto exporter = opentelemetry::exporter::trace::OStreamSpanExporterFactory::Create();
  auto processor = sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
  auto resource = opentelemetry::sdk::resource::Resource::Create(
      {{"service.name", "beacon-cpp-smoke"}});
  auto provider = sdk::TracerProviderFactory::Create(std::move(processor), resource);
  auto tracer = provider->GetTracer("beacon-cpp-smoke");
  auto span = tracer->StartSpan("beacon-cpp-smoke");
  span->End();
  return provider->Shutdown() ? 0 : 1;
}
