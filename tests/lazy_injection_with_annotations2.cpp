// expect-success
/*
 * Copyright 2014 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <fruit/fruit.h>

using fruit::Component;
using fruit::Injector;

struct Annotation1 {};
struct Annotation2 {};

struct Y {
  using Inject = fruit::Annotated<Annotation1, Y>();
  Y() {
    assert(!constructed);
    constructed = true;
  }
  
  static bool constructed;
};

using YAnnot = fruit::Annotated<Annotation1, Y>;

bool Y::constructed = false;

struct X {
  using Inject = fruit::Annotated<Annotation2, X>(fruit::Annotated<Annotation1, fruit::Provider<Y>>);
  X(fruit::Provider<Y> provider) : provider(provider) {
    assert(!constructed);
    constructed = true;
  }
  
  void run() {
    Y* y(provider);
    (void) y;
  }
  
  fruit::Provider<Y> provider;
  
  static bool constructed;
};

using XAnnot = fruit::Annotated<Annotation2, X>;

bool X::constructed = false;

fruit::Component<XAnnot> getComponent() {
  return fruit::createComponent();
}

int main() {
  
  fruit::NormalizedComponent<> normalizedComponent(fruit::createComponent());
  Injector<XAnnot> injector(normalizedComponent, getComponent());
  
  assert(!X::constructed);
  assert(!Y::constructed);
  
  X* x = injector.get<fruit::Annotated<Annotation2, X*>>();
  
  assert(X::constructed);
  assert(!Y::constructed);
  
  x->run();
  
  assert(X::constructed);
  assert(Y::constructed);
  
  return 0;
}
